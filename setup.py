# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import re
from setuptools import setup, find_packages

# Path to the __init__.py file
init_py_path = os.path.join(os.path.dirname(__file__), 'cst_python_api', '__init__.py')

# Function to extract the version number from __init__.py
def get_version():
    with open(init_py_path, 'r') as f:
        for line in f:
            match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', line)
            if match:
                return match.group(1)
    raise RuntimeError("The version number was not found in __init__.py")

# Function to extract the required packages from requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='cst_python_api',
    version=get_version(),  # Use the version number read from the __init__.py file
    packages=find_packages(),
    install_requires=read_requirements(), # Use the requirements list in requirements.txt
    author='Lucas POLO-LOPEZ',
    author_email='Lucas.Polo-Lopez@insa-rennes.fr',
    description='This module allows to control CST Microwave Studio on a Windows machine.',
    url='https://gitlab.insa-rennes.fr/hermes/cst-python-api/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    license='Mozilla Public License 2.0 (MPL 2.0)',
    python_requires='>=3.6',  # Versión mínima de Python requerida
)
