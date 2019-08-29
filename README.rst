Casearch(Aegis)
===============

Casearch is a lightweight Case Retrieve Tool. It makes things easy to retrieve
cases. It's only for internal use.

A Simple Example
----------------

.. code-block:: python

    import casearch

    c = casearch.CaseRetriever()
    res = c.retrieve_by_tag(['涉牌涉证'],
                            filter={
                                'causes': ['道路交通管理（道路）'],
                                'province': '四川省',
                                'city': '乐山市'
                            },
                            page=1,
                            size=5)
The `res` is a list contains all found documents.