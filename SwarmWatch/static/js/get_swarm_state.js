function getSwarmState() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            jQuery('#nodes').html('');
            // TODO
            // While it does shows we've got valid 200 from the backend
            // technically we might be receiving stale data and this date
            // is misleading. We should consider transmitting a datetime from
            // Python and display it here.
            jQuery('#date').html("Updated: " + new Date().toUTCString());

            let state_data = JSON.parse(this.responseText)

            for (let node_data of Object.keys(state_data)) {
                formatNode(state_data[node_data]).appendTo('#nodes')
            }
        }
    };
    xhttp.open("GET", "swarm_data", true);
    xhttp.send();
}

function formatNode(node_data) {
    let node = jQuery("<div>").attr('class', 'node text-center')

    if (node_data['status'] === "ready") {
        node.addClass('active');
    } else {
        node.addClass('inactive');
    }

    generateSimpleDiv('node-title', node_data['hostname']).appendTo(node)

    let node_rank = jQuery("<div>").attr('class', 'node-rank')
    if (node_data['manager']) {
        node_rank.html('Manager')
    } else {
        node_rank.html('Worker')
    }
    node_rank.appendTo(node);

    let node_platform = jQuery("<div>").attr('class', 'node-platform')
    if (node_data['os'] === 'windows') {
        node_platform.html('<img src="../static/img/windows.png" alt="windows logo">')
    } else {
        node_platform.html('<img src="../static/img/linux.png" alt="linux logo">')
    }
    node_platform.appendTo(node);

    let node_availability = jQuery("<div>").attr('class', 'node-availability capitalize')
    node_availability.html(node_data['availability'])
    if (node_availability.html() !== 'active') {
        node_availability.addClass('availability-not-active');
    }
    node_availability.appendTo(node);

    generateSimpleDiv('node-ip', node_data['ip']).appendTo(node)

    for (let container_data of Object.keys(node_data['containers'])) {
        if (node_data['containers'][container_data]['desired_state'] === "shutdown" &&
            node_data['containers'][container_data]['status'] !== "running") {
            /*
            Swarm data can be annoying, it still tracks historical containers that have shutdown.

            We don't care about historical containers for monitoring.

            So if a container has the desired_state of shutdown, and its status is failed/shutdown don't display it.
             */
        } else {
            formatContainer(node_data['containers'][container_data]).appendTo(node)
        }
    }

    return node
}

function formatContainer(container_data) {
    let container = jQuery("<div>").attr('class', 'container')

    if (["running", "ready"].includes(container_data['desired_state'])) {
        if (container_data['status'] === "running") {
            container.addClass('active');
        } else {
            container.addClass('preparing');
        }
    } else {
        container.addClass('inactive');
    }

    generateSimpleDiv('container-image', container_data['image']).appendTo(container)
    generateSimpleDiv('container-name', container_data['name']).appendTo(container)
    generateSimpleDiv('container-desired capitalize', container_data['desired_state']).appendTo(container)
    generateSimpleDiv('container-updated', container_data['updated']).appendTo(container)
    generateSimpleDiv('container-command', container_data['command']).appendTo(container)

    return container;
}

function generateSimpleDiv(class_name, content) {
    let div = jQuery("<div>").attr('class', class_name)
    div.html(content)
    return div
}
