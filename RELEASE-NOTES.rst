===============================
 Flask-IIIF v0.2.0 is released
===============================

Flask-IIIF v0.2.0 was released on May 22, 2015.

About
-----

Flask-IIIF is a Flask extension permitting easy integration with the
International Image Interoperability Framework (IIIF) API standards.

Incompatible changes
--------------------

- Removes `uuid_to_path_handler` callback.

- Updates error classes names (MultimediaImageResizeError and
  MultimediaImageCropError).

New features
------------

- Adds image information request endpoint `<uuid>/info.json` which
  contains available metadata for the image, such as the full height
  and width, and the functionality available for the image, such as
  the formats in which it may be retrieved, and the IIIF profile used.

- Adds new signals to REST API that permits to have access before and
  after process of the request as well as after the validation of
  IIIF.

- Adds a configurable decorator to the REST API which can be configure
  with the `api_decorator_handler`.

- Adds the `uuid_to_image_opener_handler` which can handle both
  `fullpath` and `bytestream` as source.

Improved features
-----------------

- Improves the initialisation of the REST API by adding a possibility
  to override the default API prefix `/api/multimedia/image/`.

- Adds better testing cases and increases the overall test efficiency.

Notes
-----

- The decorator can be used to restrict access to the REST API.

Installation
------------

   $ pip install Flask-IIIF

Documentation
-------------

   http://flask-iiif.readthedocs.org/en/v0.2.0

Homepage
--------

   https://github.com/inveniosoftware/flask-iiif

Happy hacking and thanks for flying Flask-IIIF.

| Invenio Development Team
|   Email: info@invenio-software.org
|   IRC: #invenio on irc.freenode.net
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://invenio-software.org
