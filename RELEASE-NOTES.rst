===============================
 Flask-IIIF v0.2.1 is released
===============================

Flask-IIIF v0.2.1 was released on April 7, 2017.

About
-----

Flask-IIIF is a Flask extension permitting easy integration with the
International Image Interoperability Framework (IIIF) API standards.

New features
------------

- Adds new signals before and after image info requests.
- Adds `dl` request parameter to specify name of file for download
  (e.g. `..default.jpg?dl=image_3.jpg`)
- Extracts image resize resampling method as a config variable.

Improved features
-----------------

- Fixes a problem where small images can trigger server errors when used with
the IIIF Presentation API.

Installation
------------

   $ pip install Flask-IIIF

Documentation
-------------

   http://flask-iiif.readthedocs.io/en/v0.2.1

Homepage
--------

   https://github.com/inveniosoftware/flask-iiif

Happy hacking and thanks for flying Flask-IIIF.

| Invenio Development Team
|   Email: info@inveniosoftware.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://inveniosoftware.org
