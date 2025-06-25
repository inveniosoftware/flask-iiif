Changes
=======

Version 1.2.1 (released 2025-06-25)

- feat: support webp images (#98)

Version 1.2.0 (released 2024-12-12)

- fix: docs reference target not found
- setup: remove werkzeug pin

Version v1.1.1 (released 2024-11-05)

- setup: remove werkzeug pin

Version v1.1.0 (released 2024-08-26)

- resize: added upscaling params for h & w

Here you can see the full list of changes between each Flask-IIIF
release.

Version 1.0.0 (released 2023-10-27)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- api: fix resize of greyscale source images
- bump flask to >=2.0, pin Werkzeug <3.0
- fix deprecated use of ``attachment_filename``

Version 0.6.3 (released 2022-07-08)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- remove custom resizing of GIF

Version 0.6.2 (released 2021-12-09)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Removes encoding of key, due to incompatibility with python3
- Makes temp folder location regarding the generation of gif files configurable
- Removes upper pinning of Werkzeug
- Closes image after usage to avoid leaking memory during api requests
- Migrates CI to gh-actions
- Updates copyright and contributors

Version 0.6.1 (released 2020-03-19)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Added missing ``app`` argument for the ``flask_iiif.cache.ImageCache``
  constructor.

Version 0.6.0 (released 2020-03-13)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Removes support for Python 2.7
- Image API specification fixes
    - Support both ``gray`` and ``grey`` as valid qualities.
    - Rotations are now performed clock-wise.
    - No padding added to resized images.
- Better support for image extension conversions (``.tif/.tiff``, ``.jp2``).
- Pillow bumped to v4.0
- Introduced ``IIIF_CACHE_IGNORE_ERRORS`` config variable to allow ignoring
  cache access exceptions.
- Changed ``current_iiif.cache`` from a callable function to a Werkzeug
  ``cached_property``.

Version 0.5.3 (released 2019-11-21)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Adds Last-Lodified and If-Modified-Since to imageapi
- Removes warning message for LocalProxy
- Fixes werkzeug deprecation warning

Version 0.5.2 (released 2019-07-25)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Sets Redis cache prefix
- Fixes cache control headers

Version 0.5.1 (released 2019-05-23)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Fixes syntax error in documentation
- Fixes import sorting

Version 0.5.0 (released 2018-05-18)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+ Fixes

  - wrong ratio calculation for best fit

+ New features

  - adds black background to requested best fit thumbnail or gif
    if the image does not cover the whole window of requested size


Version 0.4.0 (released 2018-04-17)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Fixes unicode filename issues.

- Changes default resampling algorithm to BICUBIC for better image quality.

- Adds support for _external, _scheme etc parameters for iiif_image_url.


Version 0.3.2 (released 2018-04-09)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+ Security

  - Fixed missing API protection on image metadata endpoint.

Version 0.3.1 (released 2017-08-18)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Deployment changes.

Version 0.3.0 (released 2017-08-17)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+ New features

  - Adds TIFF image support to the default config.

  - Adds proper GIF resize.

  - Adds optional Redis cache.

+ Notes

  - Minimum Pillow version is update to 3.4.

Version 0.2.0 (released 2015-05-22)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+ Incompatible changes

  - Removes `uuid_to_path_handler` callback.

  - Updates error classes names (MultimediaImageResizeError and
    MultimediaImageCropError).

+ New features

  - Adds image information request endpoint `<uuid>/info.json` which
    contains available metadata for the image, such as the full height
    and width, and the functionality available for the image, such as
    the formats in which it may be retrieved, and the IIIF profile
    used.

  - Adds new signals to REST API that permits to have access before
    and after process of the request as well as after the validation
    of IIIF.

  - Adds a configurable decorator to the REST API which can be
    configure with the `api_decorator_handler`.

  - Adds the `uuid_to_image_opener_handler` which can handle both
    `fullpath` and `bytestream` as source.

+ Improved features

  - Improves the initialisation of the REST API by adding a
    possibility to override the default API prefix
    `/api/multimedia/image/`.

  - Adds better testing cases and increases the overall test
    efficiency.

+ Notes

  - The decorator can be used to restrict access to the REST API.

Version 0.1.0 (released 2015-04-28)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Initial public release.
