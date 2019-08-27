#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: retrieve.py
# @Time: 2019/8/23 15:11


from typing import Union, List, Tuple

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from casearch import config
from casearch.log import logger


class CaseRetriever(object):

    def __init__(self,
                 hosts: Union[List[str], Tuple[str]] = config.ES_HOSTS,
                 auth_user: str = config.ES_USER,
                 auth_pwd: str = config.ES_PASSWD,
                 index: str = 'case_collection_v1',
                 doc_type: str = '_doc'):
        """
        A case casearch instance.

        :param hosts: ES hosts
        :param auth_user: ES user(if authenticated)
        :param auth_pwd: ES password(if authenticated)
        :param index: limit the search to index
        :param doc_type: only query this `_type`
        """
        self._hosts = hosts
        self._auth_user = auth_user
        self._auth_pwd = auth_pwd
        self.index = index
        self.doc_type = doc_type
        self.client = self._init_client()

    def _init_client(self):
        if self._auth_user and self._auth_pwd:
            return Elasticsearch(
                hosts=self._hosts,
                http_auth=(self._auth_user, self._auth_pwd),
                timeout=60
            )
        else:
            return Elasticsearch(self._hosts, timeout=60)

    def get_client(self):
        """
        Return a elasticsearch.Elasticsearch instance.
        """
        return self.client

    def find_by_id(self, id_: str):
        """
        Find a document by its `id`
        :param id_: field `id`
        :type id_: str
        """
        s = Search(using=self.client, index=self.index, doc_type=self.doc_type)
        s = s.query('term', id=id_)
        response = s.execute()
        if not response.hits:
            raise ValueError(f'Document with id: `{id_}` not found')
        result = response.hits[0].to_dict()
        return result

    def retrieve_by_tag(self, tag_names: list, **kwargs):
        """
        Retrieve documents by some tags' name with additional filter conditions.

        :param tag_names: the tags' name
        :type tag_names: list
        :arg filter: filter condition with `causes: list`, `province: str` and
                     `city: str` in it
        :type filter: dict
        :arg page: page number
        :type page: int
        :arg size: limit the size of each page
        :type page: int
        """
        if not tag_names:
            raise ValueError('You ought to show me some tags so that i'
                             ' can retrieve correctly.')
        page = kwargs.get('page') or 1
        size = kwargs.get('size') or 10

        # Build DSL
        tag_musts = [Q('match', fields__name=name) for name in tag_names]
        nested_q = Q('nested', path='fields', query=Q('bool', must=tag_musts))

        filter = kwargs.get('filter') or {}
        if not isinstance(filter, dict):
            raise TypeError('<filter> must be a dict containing conditions')
        causes = filter.get('causes')
        province = filter.get('province')
        city = filter.get('city')
        filter_conds = []
        if causes:
            causes_str = ' '.join(causes)
            filter_conds.append(Q('match', cause=causes_str))
        if province:
            filter_conds.append(Q('term', province=province))
        if city:
            filter_conds.append(Q('term', city=city))

        # Retrieve
        s = Search(using=self.client, index=self.index)
        s = s.query('bool',
                    must=nested_q,
                    filter=filter_conds)
        # Pagination
        s = s[(page - 1) * size:size * page]

        logger.info(f'Retriever DSL: {s.to_dict()}')
        result = [hit.to_dict() for hit in s]
        return result
