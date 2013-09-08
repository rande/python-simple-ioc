#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name="ioc",
    version="0.0.15",
    description="A small dependency injection container based on Symfony2 Dependency Component",
    author="Thomas Rabaix",
    author_email="thomas.rabaix@gmail.com",
    url="https://github.com/rande/python-simple-ioc",
    include_package_data = True,
    # py_modules=["ioc"],
    packages = find_packages(),
    install_requires=["pyyaml"],
    platforms='any',
)
