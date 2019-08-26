#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: config.py
# @Time: 2019/8/23 14:27


import os


__all__ = ['ES_HOSTS', 'ES_USER', 'ES_PASSWD']

if os.getenv('ESHOSTS'):
    host_value = os.getenv('ESHOSTS')
else:
    host_value = '127.0.0.1:9200'
ES_HOSTS = host_value.split(' ')
ES_USER = os.getenv('ESUSER')
ES_PASSWD = os.getenv('ESPASSWD')
