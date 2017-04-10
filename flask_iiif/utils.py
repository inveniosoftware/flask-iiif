# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF utilities."""
import shutil
import tempfile
from os.path import dirname, join

from flask import abort, url_for
from PIL import Image, ImageSequence

__all__ = ('iiif_image_url', )


def iiif_image_url(**kwargs):
    """Generate a `IIIF API` image url.

    :returns: `IIIF API` image url
    :rtype: str

    .. code:: html

        <img
            src="{{ iiif_image_url(uuid="id", size="200,200") }}"
            alt="Title"
        />

    .. note::

        If any IIIF parameter missing it will fall back to default:
        * `image_format = png`
        * `quality = default`
        * `region = full`
        * `rotation = 0`
        * `size = full`
        * `version = v2`
    """
    try:
        assert kwargs.get('uuid') is not None
    except AssertionError:
        abort(404)
    else:
        return url_for(
            'iiifimageapi',
            image_format=kwargs.get('image_format', 'png'),
            quality=kwargs.get('quality', 'default'),
            region=kwargs.get('region', 'full'),
            rotation=kwargs.get('rotation', 0),
            size=kwargs.get('size', 'full'),
            uuid=kwargs.get('uuid'),
            version=kwargs.get('version', 'v2'),
        )


def create_gif_from_frames(frames, duration=500, loop=0):
    """Create a GIF image.

    :param frames: the sequence of frames that resulting GIF should contain
    :param duration: the duration of each frame (in milliseconds)
    :param loop: the number of iterations of the frames (0 for infinity)
    :returns: GIF image
    :rtype: PIL.Image

    .. note:: Uses ``tempfile``, as PIL allows GIF creation only on ``save``.
    """
    # Save GIF to temporary file
    tmp = tempfile.mkdtemp(dir=dirname(__file__))
    tmp_file = join(tmp, 'temp.gif')

    head, tail = frames[0], frames[1:]
    head.save(tmp_file, 'GIF',
              save_all=True,
              append_images=tail,
              duration=duration,
              loop=loop)

    gif_image = Image.open(tmp_file)
    assert gif_image.is_animated

    # Cleanup temporary file
    shutil.rmtree(tmp)

    return gif_image


def resize_gif(image, size, resample):
    """Resize a GIF image.

    :param image: the original GIF image
    :param size: the dimensions to resize to
    :param resample: the method of resampling
    :returns: resized GIF image
    :rtype: PIL.Image
    """
    return create_gif_from_frames([frame.resize(size, resample=resample)
                                  for frame in ImageSequence.Iterator(image)])
