===============================
 Flask-IIIF v0.2.0 is released
===============================

Flask-IIIF v0.2.0 was released on May 11, 2015.

About
-----

Flask-IIIF is a Flask extension permitting easy integration with the
International Image Interoperability Framework (IIIF) API standards.

What's new
----------

- BETTER Adds better testing cases and increases the overall test
  efficiency.

- NEW Adds new signals to REST API that permits to have access before
  and after process of the request as well as after the validation of
  IIIF.

- NEW Adds a configurable decorator to the REST API which can be
  configure with the `api_decorator_handler`.

- NEW Adds the `uuid_to_image_opener_handler` which can handle both
  `fullpath` and `bytestream` as source.

Installation
------------

   $ pip install Flask-IIIF

Documentation
-------------

   http://flask-iiif.readthedocs.org/en/v0.2.0

Homepage
--------

   https://github.com/inveniosoftware/flask-iiif

Happy hacking and thanks for choosing Flask-IIIF.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://invenio-software.org
