#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='miplant',
    version='0.1.0',
    description='A library for reading cheap plant monitoring sensors manufactured by Xiaomi.',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    url='https://github.com/kipe/miplant',
    license='MIT',
    packages=[
        'miplant',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'bluepy>=1.0.5'
    ])
