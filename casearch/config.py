#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: config.py
# @Time: 2019/8/23 14:27


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Elasticsearch configurations
_host_value = os.getenv('ES_HOSTS') or '127.0.0.1:9200'
ES_HOSTS = _host_value.split(' ')
ES_USER = os.getenv('ES_USER')
ES_PASSWD = os.getenv('ES_PASSWD')

# MongoDB configurations
MONGODB_HOST = os.getenv('MONGO_HOST') or '127.0.0.1'
MONGODB_PORT = os.getenv('MONGO_PORT') or 27017
MONGODB_USER = os.getenv('MONGO_USER')
MONGODB_PASSWD = os.getenv('MONGO_PASSWD')
MONGODB_AUTH_DB = os.getenv('MONGO_AUTH_DB')
