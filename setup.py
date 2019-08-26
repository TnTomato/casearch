#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: setup.py.py
# @Time: 2019/8/23 14:07


from setuptools import setup, find_packages

setup(
    name='casearch',
    version='0.0.1',
    author='TnTomato',
    author_email='474093103@qq.com',
    description='Retrieve from ElasticSearch',
    url='https://github.com/EathonTnT/casearch',
    license='MIT',
    packages=find_packages(exclude='test'),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        'elasticsearch>=6.3.0',
        'elasticsearch_dsl>=6.3.0'
    ]
)
