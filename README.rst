============
 Flask-IIIF
============

.. image:: https://travis-ci.org/inveniosoftware/flask-iiif.png?branch=master
    :target: https://travis-ci.org/inveniosoftware/flask-iiif
.. image:: https://coveralls.io/repos/inveniosoftware/flask-iiif/badge.png?branch=master
    :target: https://coveralls.io/r/inveniosoftware/flask-iiif
.. image:: https://pypip.in/v/Flask-IIIF/badge.png
    :target: https://pypi.python.org/pypi/Flask-IIIF/
.. image:: https://pypip.in/d/Flask-IIIF/badge.png
    :target: https://pypi.python.org/pypi/Flask-IIIF/

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

Documentation is readable at http://flask-iiif.readthedocs.org or can be
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
