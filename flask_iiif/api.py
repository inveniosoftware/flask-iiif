# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia Image API."""

import itertools
import math
import os
import re

from PIL import Image
from flask import current_app
from six import BytesIO

from .errors import (
    MultmediaImageCropError, MultmediaImageResizeError,
    MultimediaImageFormatError, MultimediaImageRotateError,
    MultimediaImageQualityError, MultimediaImageNotFound,
    IIIFValidatorError
)


class MultimediaObject(object):

    """The Multimedia Object."""


class MultimediaImage(MultimediaObject):

    r"""Multimedia Image API.

    Initializes an image api with IIIF standards. You can:

    * Resize :func:`resize`.
    * Crop :func:`crop`.
    * Rotate :func:`rotate`.
    * Change image quality :func:`quality`.

    Example of editing and image and save it to disk:

    .. code-block:: python

        from flask_iiif.api import MultimediaImage

        image = IIIFImageAPIWrapper.from_file(path)
        # Rotate the image
        image.rotate(90)
        # Resize the image
        image.resize('300,200')
        # Crop the image
        image.crop('20,20,400,300')
        # Make the image black and white
        image.quality('grey')
        # Finaly save it to /tmp
        image.save('/tmp')

    Example of serving the modified image over http:

    .. code-block:: python

        from flask import current_app, Blueprint
        from flask_iiif.api import MultimediaImage

        @blueprint.route('/serve/<string:uuid>/<string:size>')
        def serve_thumbnail(uuid, size):
            \"\"\"Serve the image thumbnail.

            :param uuid: The document uuid.
            :param size: The desired image size.
            \"\"\"
            # Initialize the image with the uuid
            path = current_app.extensions['iiif'].uuid_to_path(uuid)
            image = IIIFImageAPIWrapper.from_file(path)
            # Resize it
            image.resize(size)
            # Serve it
            return send_file(image.serve(), mimetype='image/jpeg')
    """

    def __init__(self, image):
        """Initialize the image."""
        self.image = image

    @classmethod
    def from_file(cls, path):
        """Return the image object from the given path.

        :param str path: The absolute path of the file
        :returns: a :class:`~flask_iiif.api.MultimediaImage`
                  instance
        """
        if not os.path.exists(path):
            raise MultimediaImageNotFound(
                "The requested image {0} not found".format(path))

        image = Image.open(path)
        return cls(image)

    @classmethod
    def from_string(cls, source):
        """Create an :class:`~flask_iiif.api.MultimediaImage` instance.

        :param str source: The image image string
        :type source: `BytesIO` object
        :returns: a :class:`~flask_iiif.api.MultimediaImage`
                  instance
        """
        image = Image.open(source)
        return cls(image)

    def resize(self, dimensions, resample=Image.NEAREST):
        """Resize the image.

        :param str dimensions: The dimensions to resize the image
        :param resample: The algorithm to be used
        :type resample: :py:mod:`PIL.Image` algorithm

        .. note::

            * `dimensions` must be one of the following:

                * 'w,': The exact width, height will be calculated.
                * ',h': The exact height, width will be calculated.
                * 'pct:n': Image percentance scale.
                * 'w,h': The extact width and height.
                * '!w,h': Best fit for the given width and height.

        """
        real_width, real_height = self.image.size

        # Check if it is `pct:`
        if dimensions.startswith('pct:'):
            percent = float(dimensions.split(':')[1]) * 0.01
            if percent < 0:
                raise MultmediaImageResizeError(
                    ("Image percentance could not be negative, {0} has been"
                     " given").format(percent)
                )

            width = int(real_width * percent)
            height = int(real_height * percent)

        # Check if it is `,h`
        elif dimensions.startswith(','):
            height = int(dimensions[1:])
            # find the ratio
            ratio = self.reduce_by(height, real_height)
            # calculate width
            width = int(real_width * ratio)

        # Check if it is `!w,h`
        elif dimensions.startswith('!'):
            point_x, point_y = map(int, dimensions[1:].split(','))
            # find the ratio
            ratio_x = self.reduce_by(point_x, real_width)
            ratio_y = self.reduce_by(point_y, real_height)
            # take the min
            ratio = min(ratio_x, ratio_y)
            # calculate the dimensions
            width = int(point_x * ratio)
            height = int(point_y * ratio)

        # Check if it is `w,`
        elif dimensions.endswith(','):
            width = int(dimensions[:-1])
            # find the ratio
            ratio = self.reduce_by(width, real_width)
            # calculate the height
            height = int(real_height * ratio)

        # Normal mode `w,h`
        else:
            try:
                width, height = map(int, dimensions.split(','))
            except:
                raise MultmediaImageResizeError(
                    "The request must contain width,height sequence"
                )

        # If a dimension is missing throw error
        if any((dimension <= 0 and
                dimension is not None) for dimension in (width, height)):
            raise MultmediaImageResizeError(
                ("Width and height cannot be zero or negative, {0},{1} has"
                 " been given").format(width, height)
            )

        self.image = self.image.resize((width, height), resample=resample)

    def crop(self, coordinates):
        """Crop the image.

        :param str coordinates: The coordinates to crop the image

        .. note::

            * `coordinates` must have the following pattern:

                * 'x,y,w,h': in pixels.
                * 'pct:x,y,w,h': percentance.

        """
        # Get image full dimensions
        real_width, real_height = self.image.size
        real_dimensions = itertools.cycle((real_width, real_height))

        dimensions = []
        percentance = False
        if coordinates.startswith('pct:'):
            for coordinate in coordinates.split(':')[1].split(','):
                dimensions.append(float(coordinate))
            percentance = True
        else:
            for coordinate in coordinates.split(','):
                dimensions.append(int(coordinate))

        # First check if it has 4 coordinates x,y,w,h
        dimensions_length = len(dimensions)
        if dimensions_length != 4:
            raise MultmediaImageCropError(
                "Must have 4 dimensions {0} has been given".
                format(dimensions_length))

        # Make sure that there is not any negative dimension
        if any(coordinate < 0 for coordinate in dimensions):
            raise MultmediaImageCropError(
                "Dimensions cannot be negative {0} has been given".
                format(dimensions)
            )

        if percentance:
            if any(coordinate > 100.0 for coordinate in dimensions):
                raise MultmediaImageCropError(
                    "Dimensions could not be grater than 100%")

            # Calculate the dimensions
            start_x, start_y, width, height = [
                int(
                    math.floor(
                        self.percent_to_number(dimension) *
                        next(real_dimensions)
                    )
                ) for dimension in dimensions
            ]
        else:
            start_x, start_y, width, height = dimensions

        # Check if any of the requested axis is outside of image borders
        if any(axis > next(real_dimensions) for axis in (start_x, start_y)):
            raise MultmediaImageCropError(
                "Outside of image borders {0},{1}".
                format(real_width, real_height)
            )

        # Calculate the final dimensions
        max_x = start_x + width
        max_y = start_y + height
        # Check if the final width is bigger than the the real image width
        if max_x > real_width:
            max_x = real_width

        # Check if the final height is bigger than the the real image height
        if max_y > real_height:
            max_y = real_height

        self.image = self.image.crop((start_x, start_y, max_x, max_y))

    def rotate(self, degrees, mirror=False):
        """Rotate the image by given degress.

        :param float degress: The degrees, should be in range of [0, 360]
        :param bool mirror: Flip image from left to right
        """
        transforms = {
            '90': Image.ROTATE_90,
            '180': Image.ROTATE_180,
            '270': Image.ROTATE_270,
            'mirror': Image.FLIP_LEFT_RIGHT,
        }

        # Check if we have the right degress
        if not 0.0 <= float(degrees) <= 360.0:
            raise MultimediaImageRotateError(
                "Degrees must be between 0 and 360, {0} has been given".
                format(degrees)
            )

        if degrees in transforms.keys():
            self.image = self.image.transpose(transforms.get(str(degrees)))
        else:
            # transparent background if degress not multiple of 90
            self.image = self.image.convert('RGBA')
            self.image = self.image.rotate(float(degrees), expand=0)

        if mirror:
            self.image = self.image.transpose(transforms.get('mirror'))

    def quality(self, quality):
        """Change the image format.

        :param str quality: The image quality should be in (default, grey,
                        bitonal, color)

        .. note::

            The library supports transformations between each supported
            mode and the "L" and "RGB" modes. To convert between other
            modes, you may have to use an intermediate image (typically
            an "RGB" image).

        """
        qualities = current_app.config['IIIF_QUALITIES']
        if quality not in qualities:
            raise MultimediaImageQualityError(
                ("{0} does not supported, pleae select on of the"
                 " valid qualities: {1}").format(quality, qualities)
            )

        qualities_by_code = zip(qualities,
                                current_app.config['IIIF_CONVERTERS'])

        if quality not in ('default', 'color'):
            # Convert image to RGB read the note
            if self.image.mode != "RGBA":
                self.image = self.image.convert('RGBA')

            code = [quality_code[1] for quality_code in qualities_by_code
                    if quality_code[0] == quality][0]

            self.image = self.image.convert(code)

    def size(self):
        """Return the current image size.

        :return: the image size
        :rtype: list
        """
        return self.image.size

    def save(self, path, image_format="jpeg", quality=90):
        """Store the image to the specific path.

        :param str path: absolute path
        :param str image_format: (gif, jpeg, pdf, png)
        :param int quality: The image quality; [1, 100]

        .. note::

            `image_format` = jpg will not be recognized by :py:mod:`PIL.Image`
            and it will be changed to jpeg.

        """
        # transform `image_format` is lower case and not equals to jpg
        cleaned_image_format = self._prepare_for_output(image_format)
        self.image.save(path, cleaned_image_format, quality=quality)

    def serve(self, image_format="png", quality=90):
        """Return a BytesIO object to easily serve it thought HTTTP.

        :param str image_format: (gif, jpeg, pdf, png)
        :param int quality: The image quality; [1, 100]

        .. note::

            `image_format` = jpg will not be recognized by
            :py:mod:`PIL.Image` and it will be changed to jpeg.

        """
        image_buffer = BytesIO()
        # transform `image_format` is lower case and not equals to jpg
        cleaned_image_format = self._prepare_for_output(image_format)
        self.image.save(image_buffer, cleaned_image_format, quality=quality)
        image_buffer.seek(0)

        return image_buffer

    def _prepare_for_output(self, requested_format):
        """Help validate output format.

        :param str requested_format: The image output format

        .. note::

            pdf format can't be saved as `RBGA` so image needs to be converted
            to `RGB` mode.

        """
        image_format = self.sanitize_format_name(requested_format)
        format_keys = current_app.config['IIIF_FORMATS'].keys()

        if image_format not in format_keys:
            raise MultimediaImageFormatError(
                ("{0} does not supported, please select on of the valid"
                 " formats: {1}").format(requested_format, format_keys)
            )

        # If the the `requested_format` is pdf force mode to RGB
        if image_format == "pdf":
            self.image = self.image.convert('RGB')

        return image_format

    @staticmethod
    def reduce_by(nominally, dominator):
        """Calculate the ratio."""
        return float(nominally) / float(dominator)

    @staticmethod
    def percent_to_number(number):
        """Calculate the percentance."""
        return float(number) / 100.0

    @staticmethod
    def sanitize_format_name(value):
        """Lowercase formats and make sure that jpg is written as jpeg."""
        return value.lower().replace("jpg", "jpeg")


class IIIFImageAPIWrapper(MultimediaImage):

    """IIIF Image API Wrapper."""

    @staticmethod
    def validate_api(**kwargs):
        """Validate IIIF Image API.

        Example to validate the IIIF API:

        .. code:: python

            from flask_iiif.api import IIIFImageAPIWrapper

            IIIFImageAPIWrapper.validate_api(
                version=version,
                region=region,
                size=size,
                rotate=rotation,
                quality=quality,
                image_format=image_format
            )

        .. note::

            If the version is not specified it will fallback to version 2.0.

        """
        # Get the api version
        version = kwargs.get('version', 'v2')
        # Get the validations and ignore cases
        cases = current_app.config['IIIF_VALIDATIONS'].get(version)
        for key in cases.keys():
            # If the parameter don't match with iiif casess
            if not re.search(
                    cases.get(key, {}).get('validate', ''), kwargs.get(key)
            ):
                raise IIIFValidatorError(
                    ("value: `{0}` for parameter: `{1}` is not supported").
                    format(kwargs.get(key), key)
                )

    def apply_api(self, **kwargs):
        """Apply the IIIF API to the image.

        Example to apply the IIIF API:

        .. code:: python

            from flask_iiif.api import IIIFImageAPIWrapper

            image = IIIFImageAPIWrapper.from_file(path)

            image.apply_api(
                version=version,
                region=region,
                size=size,
                rotate=rotation,
                quality=quality
            )

        .. note::

            * If the version is not specified it will fallback to version 2.0.
            * Please note the :func:`validate_api` should be ran before
              :func:`apply_api`.

        """
        # Get the api version
        version = kwargs.get('version', 'v2')
        # Get the validations and ignore cases
        cases = current_app.config['IIIF_VALIDATIONS'].get(version)
        # Set the apply order
        order = 'region', 'size', 'rotate', 'quality'
        # Set the functions to be applied
        tools = {
            "region": self.apply_region,
            "size": self.apply_size,
            "rotate": self.apply_rotate,
            "quality": self.apply_quality
        }

        for key in order:
            # Ignore if has the ignore value for the specific key
            if kwargs.get(key) != cases.get(key, {}).get('ignore'):
                tools.get(key)(kwargs.get(key))

    def apply_region(self, value):
        """IIIF apply crop.

        Apply :func:`~flask_iiif.api.MultimediaImage.crop`.
        """
        self.crop(value)

    def apply_size(self, value):
        """IIIF apply resize.

        Apply :func:`~flask_iiif.api.MultimediaImage.resize`.
        """
        self.resize(value)

    def apply_rotate(self, value):
        """IIIF apply rotate.

        Apply :func:`~flask_iiif.api.MultimediaImage.rotate`.
        """
        mirror = False
        degrees = value
        if value.startswith('!'):
            mirror = True
            degrees = value[1:]
        self.rotate(degrees, mirror=mirror)

    def apply_quality(self, value):
        """IIIF apply quality.

        Apply :func:`~flask_iiif.api.MultimediaImage.quality`.
        """
        self.quality(value)
