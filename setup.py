#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    'requests',
    'bs4',
    'lxml'
]


setup(
    name = "douban-export",
    version = "0.0.1",
    author = "Ein Verne",
    author_email = "git@einverne.info",
    description = "A tool to help export douban data ",
    license = "MIT",
    keywords = "douban, export, command, tools",
    url = "https://github.com/einverne/douban-export",
    packages=find_packages(exclude=["test"]),
    long_description=read('README.md'),
    include_package_data=True,
    install_requires=requirements,
    entry_points={'console_scripts': ['douban=src.__main__:main']},
)