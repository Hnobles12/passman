#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='passman',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
        'toml',
        'TinyDB',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'passman = passman:app',
        ],
    },
)
