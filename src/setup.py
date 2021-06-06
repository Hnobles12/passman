#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='passman',
    version='0.1.0',
    py_modules=['passman'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'passman = passman:app',
        ],
    },
)
