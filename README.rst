.. image:: https://img.shields.io/pypi/v/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.formsupport.counter.svg?style=plastic
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: License

.. image:: https://coveralls.io/repos/github/collective/collective.formsupport.counter/badge.svg
    :target: https://coveralls.io/github/collective/collective.formsupport.counter
    :alt: Coverage


==============================
collective.formsupport.counter
==============================

Counter integration for `collective.volto.formsupport <https://github.com/collective/collective.volto.formsupport>`_

Features
--------

- Form counter for `collective.volto.formsupport <https://github.com/collective/collective.volto.formsupport>`_ >= 3.2


Installation
------------

Install collective.formsupport.counter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.formsupport.counter


and then running ``bin/buildout``

REST API
========

Here is the list of available REST API endpoints and how to use them.

1. **Reset form counter**

   - **Endpoint**: `/<document>/@reset-counter`.
   - **Method**: `PATCH`.
   - **Parameters**: `block_id` form block identifier.
   - **Description**: Reset form counter.
   - **Request**: No parameters required.
   - **Response**:

     - **Status Code**: `204 No Content`

Authors
-------

RedTurtle


Contributors
------------

- folix-01

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.formsupport.counter/issues
- Source Code: https://github.com/collective/collective.formsupport.counter
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@redturtle.it


License
-------

The project is licensed under the GPLv2.
