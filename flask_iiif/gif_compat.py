# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF frame-preserving GIF operations."""

import types

from PIL import Image, ImageSequence
from six import BytesIO

__all__ = ('apply_image_operation', 'create_gif_from_frames', 'is_gif_image')


def is_gif_image(image):
    """Test whether a PIL image is formatted as GIF."""
    return image.format == 'GIF'


def create_gif_from_frames(frames, duration=500, loop=0):
    """Create a GIF image.

    :param frames: the sequence of frames that the resulting GIF should contain
    :param duration: the duration of each frame (in milliseconds)
    :param loop: the number of iterations of the frames (0 for infinity)
    :returns: GIF image
    :rtype: PIL.Image
    """
    tmp_file = BytesIO()
    head, tail = frames[0], frames[1:]
    head.save(tmp_file, 'GIF',
              save_all=True, append_images=tail,
              duration=duration, loop=loop)

    gif_image = Image.open(tmp_file)
    assert is_gif_image(gif_image)
    return gif_image


def patch_image(image):
    """Patch PIL.Image operations for the GIF format."""
    if is_gif_image(image):
        methods = ['save', 'resize', 'crop', 'transpose', 'rotate']
        for method_name in methods:
            _patch_method(image, method_name)
    return image


def _patch_method(instance, method_name):
    """Patch a method of PIL.Image to make it compatible with GIF images."""
    if method_name == 'save':
        default_save = instance.save

        def gif_save(self, *args, **kwargs):
            kwargs.setdefault('save_all', True)
            return default_save(*args, **kwargs)

        instance.save = types.MethodType(gif_save, instance)

    else:
        def gif_method(self, *args, **kwargs):
            frames = [getattr(f, method_name)(*args, **kwargs)
                      for f in _generate_gif_frames(self)]
            return create_gif_from_frames(frames,
                                          duration=self.info['duration'],
                                          loop=self.info['loop'])

        setattr(instance, method_name, types.MethodType(gif_method, instance))


def _generate_gif_frames(gif_image):
    """Generate frames of a GIF image as PNG images."""
    for i, frame in enumerate(ImageSequence.Iterator(gif_image)):
        tmp = BytesIO()
        frame.save(tmp, format='PNG', save_all=False)
        yield Image.open(tmp)
