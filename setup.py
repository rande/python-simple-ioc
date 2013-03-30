#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="ioc",
    version="0.0.5",
    description="A small dependency injection container based on Symfony2 Dependency Component",
    author="Thomas Rabaix",
    author_email="thomas.rabaix@gmail.com",
    url="https://github.com/rande/python-simple-ioc",
    py_modules=["ioc"],
    packages = ['ioc'],
    install_requires=["pyyaml"],
)
