# SPDX-FileCopyrightText: 2014, 2015 CERN.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: BSD-3-Clause

"""Multimedia error."""


class MultimediaError(Exception):
    """General multimedia exception."""

    def __init__(self, message=None, code=None):
        """Init the error handler."""
        super(MultimediaError, self).__init__()
        self.message = message or self.__class__.__name__
        self.code = code or 500

    def __str__(self):
        """Error message."""
        return repr(
            "Error message: {message}. Error code: {code}".format(
                message=self.message, code=self.code
            )
        )


class MultimediaImageNotFound(MultimediaError):
    """Image not found error."""

    def __init__(self, message=None, image=None):
        """Init with status code 404."""
        super(MultimediaImageNotFound, self).__init__(message, code=404)
        self.image = image


class MultimediaImageCropError(MultimediaError):
    """Image on crop error."""


class MultimediaImageResizeError(MultimediaError):
    """Image resize error."""


class MultimediaImageRotateError(MultimediaError):
    """Image rotate error."""

    def __init__(self, message=None, degrees=None):
        """Init with status code 400 and further details."""
        super().__init__(message, code=400)
        self.degrees = degrees


class MultimediaImageQualityError(MultimediaError):
    """Image quality error."""

    def __init__(self, message=None, requested_quality=None, supported_qualities=None):
        """Init with status code 400 and further details."""
        super().__init__(message, code=400)
        self.requested_quality = requested_quality
        self.supported_qualities = supported_qualities


class MultimediaImageFormatError(MultimediaError):
    """Image format error."""

    def __init__(self, message=None, requested_format=None, supported_formats=None):
        """Init with status code 400 and further details."""
        super().__init__(message, code=400)
        self.requested_format = requested_format
        self.supported_formats = supported_formats


class IIIFValidatorError(MultimediaError):
    """IIIF API validator error."""

    def __init__(self, message=None, parameter=None, value=None):
        """Init with status code 400 and further details."""
        super().__init__(message, code=400)
        self.parameter = parameter
        self.value = value
