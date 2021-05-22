import setuptools

with open('README.md', 'r', encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='SwarmWatch',
    version='1.0',
    description="SwarmWatch is a library for visualizing a Docker Swarm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='BinaryHabitat',
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    python_requires='>=3.8',
    project_urls={
        'Source': 'https://github.com/binaryhabitat/SwarmWatch'
    },
    install_requires=[
        'Flask>=1.1.2, <2.0',
        'python-dateutil',
        'docker>=5'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)'
    ],
    zip_safe=False
)
