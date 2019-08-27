#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: log.py
# @Time: 2019/8/27 10:13


import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt="%y-%m-%d %H:%M:%S",
                    level=logging.INFO)

logger = logging.getLogger()
