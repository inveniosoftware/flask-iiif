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
        url_for_args = {k: v for k, v in kwargs.items() if k.startswith('_')}

        return url_for(
            'iiifimageapi',
            image_format=kwargs.get('image_format', 'png'),
            quality=kwargs.get('quality', 'default'),
            region=kwargs.get('region', 'full'),
            rotation=kwargs.get('rotation', 0),
            size=kwargs.get('size', 'full'),
            uuid=kwargs.get('uuid'),
            version=kwargs.get('version', 'v2'),
            **url_for_args
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


def resize_with_background_gif(image, size, resample, demand_w=0, demand_h=0):
    """Resize a GIF image and fills the missing pixels with black background.

    :param image: the original GIF image
    :param size: the dimensions to resize to
    :param resample: the method of resampling
    :param demand_w: demanded height for thumbnail
    :param demand_h: demanded width for thumbnail
    :returns: resized GIF image
    :rtype: PIL.Image
    """
    return create_gif_from_frames([fill_background(
        frame.resize(size, resample=resample), demand_w, demand_h)
        for frame in ImageSequence.Iterator(image)])


def fill_background(image, demand_width, demand_height):
    """Fill the background with black (in case of image too small).

    :param image: image which does not fit into the window
    :param demand_width: demanded thumbnail window width
    :param demand_height: demanded window height
    :returns: image of requested size, filled with black background
    :rtype: PIL.Image
    """
    background = Image.new('RGB', (demand_width, demand_height))
    offset_x, offset_y = 0, 0
    w, h = image.size
    if w < demand_width:
        # set the image in the middle of x axis
        offset_x = max(1, int((demand_width - w) / 2))
    if h < demand_height:
        # set the image in the middle of y axis
        offset_y = max(1, int((demand_height - h) / 2))
    background.paste(image, (offset_x, offset_y))
    return background
