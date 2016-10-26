#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='miplant',
    version='0.0.1',
    description='A library for reading cheap plant monitoring sensors manufactured by Xiaomi.',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    url='https://github.com/kipe/miplant',
    packages=[
        'miplant',
    ],
    install_requires=[
        'gattlib>=0.20150805',
    ])
