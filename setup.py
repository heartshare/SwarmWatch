"""
Copyright (C) 2021 https://github.com/binaryhabitat.

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

from setuptools import find_packages, setup

setup(
    install_requires=[
        "Flask >=1.1.2, <2.0",
        "python-dateutil",
        "docker >=5"
    ],
    extras_require={
        "dev": [
            "isort",
            "pyquotes",
            "wheel"
        ]
    },
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*"
        ]
    ),
    python_requires=">=3.9",
    zip_safe=False
)
