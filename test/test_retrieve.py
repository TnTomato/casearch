#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: test_retrieve.py
# @Time: 2019/8/26 11:06


import pytest

import casearch


def test_retrieve_by_tag():
    c = casearch.CaseRetriever()
    res = c.retrieve_by_tag(['涉牌涉证'],
                            filter={
                                'causes': ['道路交通管理（道路）'],
                                'province': '四川省',
                                'city': '乐山市'
                            },
                            page=1,
                            size=5)
    assert isinstance(res, list)
