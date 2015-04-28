============
 Flask-IIIF
============
.. currentmodule:: flask_iiif


.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/flask-iiif">
            <img src="https://travis-ci.org/inveniosoftware/flask-iiif.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/flask-iiif">
            <img src="https://coveralls.io/repos/inveniosoftware/flask-iiif/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>


Flask-IIIF is a Flask extension permitting easy integration with the
International Image Interoperability Framework (IIIF) API standards.

Contents
--------

.. contents::
   :local:
   :backlinks: none


Installation
============

Flask-IIIF is on PyPI so all you need is :

.. code-block:: console

    $ pip install flask-iiif

The development version can be downloaded from `its page at GitHub
<http://github.com/inveniosoftware/flask-iiif>`_.

.. code-block:: console

    $ git clone https://github.com/inveniosoftware/flask-iiif.git
    $ cd flask-iiif
    $ python setup.py develop
    $ ./run-tests.sh

Requirements
^^^^^^^^^^^^

Flask-IIIF has the following dependencies:

* `Flask <https://pypi.python.org/pypi/Flask>`_
* `blinker <https://pypi.python.org/pypi/blinker>`_
* `six <https://pypi.python.org/pypi/six>`_

Flask-IIIF requires Python version 2.6, 2.7 or 3.3+


Quickstart
==========

This part of the documentation will show you how to get started in using
Flask-IIIF with Flask.

This guide assumes you have successfully installed Flask-IIIF and a working
understanding of Flask. If not, follow the installation steps and read about
Flask at http://flask.pocoo.org/docs/.


A Minimal Example
^^^^^^^^^^^^^^^^^

A minimal Flask-IIIF usage example looks like this.

First, let's create the application and initialise the extension:

.. code-block:: python

    from flask import Flask, session, redirect
    from flask_iiif import IIIF
    app = Flask("myapp")
    ext = IIIF(app=app)


Second, let's create *Flask-RESTful* ``api`` instance and register image
resource.

.. code-block:: python

    from flask_restful import Api
    api = Api(app=app)
    ext.init_restful(api)


Configuration
=============

.. automodule:: flask_iiif.config
    :members:

API
===

This documentation section is automatically generated from Flask-IIIF's
source code.

Flask-IIIF
^^^^^^^^^^

.. automodule:: flask_iiif.api
    :members:

Cache
^^^^^

.. automodule:: flask_iiif.cache.cache
    :members:

.. automodule:: flask_iiif.cache.simple
    :members:

RESTful
^^^^^^^

.. automodule:: flask_iiif.restful
    :members:

.. include:: ../CHANGES

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS
