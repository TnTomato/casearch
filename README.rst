Casearch(Aegis)
===============

Casearch is a lightweight Case Retrieve Tool. It makes things easy to retrieve
cases. It's only for internal use.

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