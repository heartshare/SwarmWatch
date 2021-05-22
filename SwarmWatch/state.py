import docker
import time
import sys
import threading
import re
from dateutil import parser
from typing import List


class SwarmState:
    def __init__(self):
        self.json = {}
        self._client = docker.APIClient(base_url=self._get_docker_url())

        # TODO: Currently, nothing will clean this thread up
        self._update_thread = threading.Thread(target=self.update)
        self._update_thread.start()

    def update(self) -> None:
        while True:
            time.sleep(0.5)  # This is obviously not an exact science.

            data = {}

            # Gather node metadata
            for node in self._client.nodes():
                try:
                    data[node['ID']] = self.node_factory(node)
                except KeyError:
                    continue

            # Each container factory needs access to the service list, by acquiring it here
            # we stop ourselves needing to query the Docker daemon on each container factory
            services = self._client.services()
            # Gather container metadata and append to the host node
            for task in self._client.tasks():
                try:
                    data[task['NodeID']]['containers'].append(self.container_factory(task, services))
                except KeyError:
                    continue

            self.json = data

    @staticmethod
    def container_factory(container: dict, services: List[dict]) -> dict:
        for service in services:
            if service['ID'] == container['ServiceID']:
                container_name = f"{service['Spec']['Name']}.{container['Slot']}"
                break
        else:
            container_name = container.get('ServiceID', 'UNKNOWN')

        return {'id': container.get('ID'),
                'name': container_name,
                'updated': parser.isoparse(container.get('UpdatedAt', '')).strftime("%H:%M:%S (%d %B)"),
                'image': re.split("@", container.get('Spec', {}).get('ContainerSpec', {}).get('Image', '?'), 1)[0],
                'service_id': container.get('ServiceID'),
                'desired_state': container.get('DesiredState'),
                'status': container.get('Status', {}).get('State'),
                'command': " ".join(container.get('Spec', {}).get('ContainerSpec', {}).get('Args', [' ']))}

    @staticmethod
    def node_factory(node: dict) -> dict:
        return {'id': node['ID'],
                'hostname': node['Description']['Hostname'],
                'status': node['Status']['State'],
                'availability': node['Spec']['Availability'],
                'manager': node['Spec']['Role'] in ('manager', 'leader'),
                'os': node['Description']['Platform']['OS'],
                'ip': node['Status']['Addr'],
                'containers': []}

    @staticmethod
    def _get_docker_url() -> str:
        # Expecting to deal with daemon exposed to this application, via either of these means
        return 'npipe:////./pipe/docker_engine' if sys.platform == 'win32' else 'unix:///var/run/docker.sock'
