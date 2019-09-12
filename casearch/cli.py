#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ZhangXiaocheng
# @File: cli.py
# @Time: 2019/8/27 14:15


import multiprocessing
from ctypes import c_char_p
from multiprocessing import Pool, Value
from urllib.parse import quote_plus

import click
from bson.objectid import ObjectId
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import NotFoundError, RequestError
from pymongo import MongoClient

from casearch.config import (
    ES_HOSTS, ES_USER, ES_PASSWD, MONGODB_HOST, MONGODB_PORT, MONGODB_USER,
    MONGODB_PASSWD, MONGODB_AUTH_DB
)

_DEFAULT_WORKER = multiprocessing.cpu_count()

if not MONGODB_USER and not MONGODB_PASSWD and not MONGODB_AUTH_DB:
    _mongo_uri = f'mongodb://{MONGODB_HOST}:{MONGODB_PORT}'
else:
    _mongo_uri = f'mongodb://{quote_plus(MONGODB_USER)}:{quote_plus(MONGODB_PASSWD)}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_AUTH_DB}'

_mapping = {
    'mappings': {
        '_doc': {
            'properties': {
                'id': {
                    'type': 'keyword'
                },
                'title': {
                    'type': 'text',
                    'analyzer': 'smart_analyzer'
                },
                'decide_date': {
                    'type': 'date',
                    'format': 'yyyy-MM-dd'
                },
                'doc_type': {
                    'type': 'keyword'
                },
                'judicial_officers': {
                    'type': 'text',
                    'analyzer': 'whitespace'
                },
                'attorney': {
                    'type': 'nested',
                    'properties': {
                        'name': {
                            'type': 'keyword'
                        },
                        'lawoffice': {
                            'type': 'text',
                            'analyzer': 'smart_analyzer'
                        }
                    }
                },
                'court': {
                    'type': 'text',
                    'analyzer': 'smart_analyzer'
                },
                'trial_round': {
                    'type': 'keyword'
                },
                'cause': {
                    'type': 'text',
                    'analyzer': 'whitespace'
                },
                'case_number': {
                    'type': 'keyword'
                },
                'case_number_year': {
                    'type': 'integer'
                },
                'accuser': {
                    'type': 'text',
                    'analyzer': 'whitespace'
                },
                'accused': {
                    'type': 'text',
                    'analyzer': 'whitespace'
                },
                'paras': {
                    'type': 'nested',
                    'properties': {
                        'tag': {
                            'type': 'keyword'
                        },
                        'content': {
                            'type': 'text',
                            'analyzer': 'smart_analyzer'
                        }
                    }
                },
                'fulltext': {
                    'type': 'text',
                    'analyzer': 'smart_analyzer'
                },
                'province': {
                    'type': 'keyword'
                },
                'city': {
                    'type': 'keyword'
                },
                'top_cause': {
                    'type': 'keyword'
                },
                'codes': {
                    'type': 'nested',
                    'properties': {
                        'code_name': {
                            'type': 'text',
                            'analyzer': 'smart_analyzer'
                        },
                        'clauses': {
                            'type': 'text',
                            'analyzer': 'whitespace'
                        }
                    }
                },
                'fields': {
                    'type': 'nested',
                    'properties': {
                        'name': {
                            'type': 'keyword'
                        },
                        'value': {
                            'type': 'float'
                        }
                    }
                }
            }
        }
    }
}


def _get_es():
    es = Elasticsearch(
        hosts=ES_HOSTS,
        http_auth=(ES_USER, ES_PASSWD),
        timeout=60
    )
    return es


def _get_docs(coll, query=None, projection=None, size=100, oid=None):
    if query is None:
        query = {}
    if oid:
        _id = oid.value.decode('utf-8')
        query.update({'_id': {'$gt': ObjectId(_id)}})
    if projection:
        cursor = coll.find(filter=query, projection=projection)
    else:
        cursor = coll.find(query)
    documents = []
    i = 0
    for doc in cursor:
        documents.append(doc)
        i += 1
        if i == size:
            yield documents
            last_oid = str(doc['_id'])
            oid.value = last_oid.encode('utf-8')
            documents = []
            i = 0


def _run(case_docs, db, field, index, type):
    _client = MongoClient(_mongo_uri)
    case_db = _client[db]
    field_coll = case_db[field]
    es = _get_es()
    case_ids = [doc.get('id') for doc in case_docs if doc.get('id')]
    field_docs = field_coll.find({'id': {'$in': case_ids}})
    mapping = {}
    for doc in field_docs:
        fields = []
        for field_id, field in doc['fields'].items():
            value = field.get('value')
            es_name = field.get('name')
            if not value:
                es_value = 1.0
            else:
                for i in value:
                    es_value = i.get('金额') or i.get('数量')
                    break
                else:
                    es_value = 1.0
            fields.append({
                'name': es_name,
                'value': es_value
            })
        mapping.update({doc['id']: fields})

    actions = []
    for doc in case_docs:
        try:
            case_id = doc['id']
        except KeyError:
            continue
        else:
            case_ids.append(case_id)

        source = {
            'id': case_id
        }

        title = doc.get('title')
        if not title:
            continue
        else:
            source['title'] = title

        decide_date = doc.get('decide_time')
        if not decide_date:
            continue
        else:
            source['decide_date'] = decide_date

        doc_type = doc.get('doc_type')
        if not doc_type:
            continue
        else:
            source['doc_type'] = doc_type

        court = doc.get('court')
        if not court:
            continue
        else:
            source['court'] = court

        trial_round = doc.get('trial_round')
        if not trial_round:
            continue
        else:
            source['trial_round'] = trial_round

        case_number = doc.get('case_number')
        if not case_number:
            continue
        else:
            source['case_number'] = case_number

        case_number_year = doc.get('case_number_year')
        if not case_number_year:
            continue
        else:
            source['case_number_year'] = case_number_year

        paras = doc.get('paras')
        if not paras:
            continue
        else:
            source['paras'] = paras

        province = doc.get('province')
        if not province:
            continue
        else:
            source['province'] = province

        city = doc.get('city')
        if not city:
            continue
        else:
            source['city'] = city

        top_cause = doc.get('top_cause')
        if not top_cause:
            continue
        else:
            source['top_cause'] = top_cause

        codes = doc.get('codes')
        if not codes:
            continue
        else:
            try:
                es_codes = [
                    {
                        'code_name': code['code_name'][0],
                        'clauses': ' '.join(code['clauses'])
                    } for code in codes
                ]
            except (KeyError, IndexError):
                continue
            else:
                source['codes'] = es_codes

        cause = doc.get('cause')
        if not cause:
            continue
        else:
            if isinstance(cause, list):
                source['cause'] = ' '.join(cause)
            else:
                continue

        party = doc.get('party')
        if not party:
            continue
        else:
            if isinstance(party, list):
                accusers = []
                accuseds = []
                for i in party:
                    name = i.get('name')
                    if i.get('type') == '原告':
                        if name:
                            accusers.append(name)
                    elif i.get('type') == '被告':
                        if name:
                            accuseds.append(name)
                    else:
                        continue
                if accusers:
                    source['accuser'] = ' '.join(accusers)
                if accuseds:
                    source['accused'] = ' '.join(accuseds)

        if mapping.get(case_id):
            source['fields'] = mapping[case_id]
        else:
            continue

        action = {
            '_index': index,
            '_type': type,
            '_id': doc['id'],
            '_source': source
        }
        actions.append(action)
    res = helpers.bulk(es, actions)
    click.echo(f'Success and failure: {res}')


@click.group()
def cli():
    pass


@cli.command('index', short_help='Create an index.')
@click.option(
    '--name',
    '-n',
    default='case_collection_v1',
    help='Name of index.'
)
@click.option(
    '--shard',
    '-s',
    default=5,
    help='Number of shards of the index.'
)
@click.option(
    '--replica',
    '-r',
    default=0,
    help='Number of replicas of the index.'
)
def create_index(name, shard, replica):
    es = _get_es()
    _settings = {
        'settings': {
            'number_of_shards': shard,
            'number_of_replicas': replica,
            'analysis': {
                'analyzer': {
                    'max_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'ik_max_word',
                        'char_filter': [
                            'html_strip'
                        ]
                    },
                    'smart_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'ik_smart',
                        'char_filter': [
                            'html_strip'
                        ]
                    }
                }
            }
        }
    }
    _mapping.update(_settings)
    try:
        es.indices.create(index=name, body=_mapping)
    except RequestError as e:
        click.echo(f'Error: {e.info["error"]["reason"]}, '
                   f'the option is canceled.')
    else:
        click.echo(f'Index `{name}` created!')


@cli.command('drop', short_help='Drop the index matches the given name.')
@click.option('--name', '-n', help='Name of the index.')
@click.confirmation_option(
    prompt='Are you sure you want to drop this index?'
)
def drop_index(name):
    es = _get_es()
    try:
        es.indices.delete(index=name)
    except NotFoundError as e:
        click.echo(f'Error: {e.info["error"]["reason"]}, '
                   f'the option is canceled.')
    else:
        click.echo(f'Index `{name}` deleted!')


@cli.command(
    'sync',
    short_help='Sync data from MongoDB to Elasticsearch.'
)
@click.option(
    '--worker',
    '-w',
    default=_DEFAULT_WORKER,
    help='Number of workers.'
)
@click.option('--size', '-s', default=1000, help='Size of data.')
@click.option(
    '--db',
    default='xcase_parse',
    help='The database\'s name in MongoDB.'
)
@click.option(
    '--case',
    default='case_collection',
    help='Collection of cases in MongoDB.'
)
@click.option(
    '--field',
    default='case_collection_fields',
    help='Collection of fields in MongoDB.'
)
@click.option(
    '--index',
    default='case_collection_v1',
    help='Index of Elasticsearch.'
)
@click.option(
    '--type',
    default='_doc',
    help='_type in Elasticsearch'
)
@click.option(
    '--flag',
    default=None,
    help='The string type of _id in MongoDB marked as a start flag.'
)
def sync(worker, size, db, case, field, index, type, flag):
    _client = MongoClient(_mongo_uri)
    case_db = _client[db]
    case_coll = case_db[case]
    num_of_process = worker
    if flag:
        first_id = flag
    else:
        first_id = str(case_coll.find()[0]['_id'])
    oid = Value(c_char_p, first_id.encode('utf-8'))
    pool = Pool(num_of_process)
    for docs in _get_docs(case_coll,
                          projection={
                              'attorney': 0,
                              'child_trial_round': 0,
                              'es_index_name': 0,
                              'judgement_result': 0,
                              'judicial_officers': 0,
                          },
                          size=size,
                          oid=oid):
        pool.apply_async(_run, (docs, db, field, index, type))
    pool.close()
    pool.join()


command = click.CommandCollection(sources=[cli])

if __name__ == '__main__':
    command()
