Casearch(Aegis)
===============

Casearch is a lightweight Case Retrieve Tool. It makes things easy to retrieve
cases. It's only for internal use.

Configuration
-------------

It is recommanded to add some configuration information as your environment
variables. The variable is as follow::
    ESHOSTS: Elasticsearch cluster address, they must be separated by white space.
    ESUSER: Elasticsearch's http_auth username.
    ESPASSWD: Elasticsearch's http_auth password.
    MONGOHOST: MongoDB's host.
    MONGOPORT: MongoDB's port.
    MONGOUSER: MongoDB's user(if authenticated).
    MONGOPASSWD: MongoDB's password(if authenticated).
    MONGODB: MongoDB's authentication DB(if authenticated).

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
