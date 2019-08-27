#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: setup.py.py
# @Time: 2019/8/23 14:07


import io
import re

from setuptools import setup, find_packages

with io.open('README.rst', 'rt', encoding='utf-8') as f:
    readme = f.read()

with io.open('casearch/__init__.py', 'rt', encoding='utf-8') as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)

setup(
    name='casearch',
    version=version,
    author='TnTomato',
    author_email='474093103@qq.com',
    description='Retrieve from ElasticSearch',
    url='https://github.com/EathonTnT/casearch',
    license='MIT',
    packages=find_packages(exclude='test'),
    python_requires='>=3.6',
    install_requires=[
        'elasticsearch>=6.3.0',
        'elasticsearch_dsl>=6.3.0',
        'click>=7.0',
        'pymongo>=3.0.0',
        'python-dotenv>=0.10.0'
    ],
    entry_points={
        'console_scripts': ['casearch = casearch.cli:command']
    }
)
