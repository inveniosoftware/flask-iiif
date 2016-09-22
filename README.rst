============
 Flask-IIIF
============

.. image:: https://img.shields.io/travis/inveniosoftware/flask-iiif.svg
        :target: https://travis-ci.org/inveniosoftware/flask-iiif

.. image:: https://img.shields.io/coveralls/inveniosoftware/flask-iiif.svg
        :target: https://coveralls.io/r/inveniosoftware/flask-iiif

.. image:: https://img.shields.io/github/tag/inveniosoftware/flask-iiif.svg
        :target: https://github.com/inveniosoftware/flask-iiif/releases

.. image:: https://img.shields.io/pypi/dm/flask-iiif.svg
        :target: https://pypi.python.org/pypi/flask-iiif

.. image:: https://img.shields.io/github/license/inveniosoftware/flask-iiif.svg
        :target: https://github.com/inveniosoftware/flask-iiif/blob/master/LICENSE

About
=====

Flask-IIIF is a Flask extension permitting easy integration with the
International Image Interoperability Framework (IIIF) API standards.

Installation
============

Flask-IIIF is on PyPI so all you need is: ::

    pip install Flask-IIIF

Documentation
=============

Documentation is readable at http://flask-iiif.readthedocs.io or can be
built using Sphinx: ::

    git submodule init
    git submodule update
    pip install Sphinx
    python setup.py build_sphinx

Testing
=======
Running the test suite is as simple as: ::

    python setup.py test

or, to also show code coverage: ::

    ./run-tests.sh
