# -*- coding: utf-8 -*-
"""
Setup file for tenma package.
@author: Diogo Fonseca
"""

from setuptools import setup, find_packages

setup(
    name='powersupply',
    version='0.1.0',
    description='Python interface for laboratory power supplies',
    author='Diogo',
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.5'
    ],
)