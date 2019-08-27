#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: config.py
# @Time: 2019/8/23 14:27


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if os.getenv('ESHOSTS'):
    host_value = os.getenv('ESHOSTS')
else:
    host_value = '127.0.0.1:9200'
ES_HOSTS = host_value.split(' ')
ES_USER = os.getenv('ESUSER')
ES_PASSWD = os.getenv('ESPASSWD')

MONGODB_HOST = os.getenv('MONGOHOST') or '127.0.0.1'
MONGODB_PORT = os.getenv('MONGOPORT') or 27017
MONGODB_USER = os.getenv('MONGOUSER')
MONGODB_PASSWD = os.getenv('MONGOPASSWD')
MONGODB_DB = os.getenv('MONGODB')
