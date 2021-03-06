#!/usr/bin/env python

"""
    Protean - A prometheus client.
"""

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="protean",
    version="0.1",
    author="Joao Grilo",
    author_email="joao.grilo@gmail.com",
    description="Generate promteheus metrics",
    license="MIT",
    keywords="actor framework",
    url="https://github.com/grilo/protean",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'hollywood',
    ],
    dependency_links=[
        'git+https://github.com/grilo/hollywood.git#egg=hollywood'
    ],
    tests_require=['pytest-runner', 'pylint', 'pytest', 'pytest-cov', 'pytest-mock'],
)
