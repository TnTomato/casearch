Casearch(Aegis)
===============

Casearch is a lightweight Case Retrieve Tool. It makes things easy to retrieve
cases. It's only for internal use.

Configuration
-------------

It is recommanded to add some configuration information as your environment
variables. The variable is as follow::
    ES_HOSTS: Elasticsearch cluster address, they must be separated by white space.
    ES_USER: Elasticsearch's http_auth username.
    ES_PASSWD: Elasticsearch's http_auth password.
    MONGO_HOST: MongoDB's host.
    MONGO_PORT: MongoDB's port.
    MONGO_USER: MongoDB's user(if authenticated).
    MONGO_PASSWD: MongoDB's password(if authenticated).
    MONGO_AUTH_DB: MongoDB's authentication DB(if authenticated).

A Simple Example
----------------

.. code-block:: python

    import casearch

    c = casearch.CaseRetriever()
    res = c.retrieve_by_tag(['tag_name'],
                            filter={
                                'causes': ['cause_name'],
                                'province': 'province_name',
                                'city': 'city_name'
                            },
                            page=1,
                            size=5)
    print(res)

The output is a list contains all found documents.

Command
-------

Get help from the command line::

    $ casearch --help

sync
````

Get help with::

    $ casearch sync --help
