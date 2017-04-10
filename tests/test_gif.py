# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""GIF Tests."""

from PIL import Image
from six import BytesIO

from flask_iiif.gif_compat import create_gif_from_frames, patch_image

from .helpers import IIIFTestCase


class TestGIF(IIIFTestCase):

    """GIF test case."""

    def check_gif(self, gif, size=(1280, 1024), n_frames=5):
        """Check if gif is animated and has desired properties."""
        self.assertEqual(gif.format, 'GIF')
        self.assertEqual(gif.is_animated, True)
        self.assertEqual('duration' in gif.info, True)
        self.assertEqual('loop' in gif.info, True)
        self.assertEqual(gif.size, size)
        self.assertEqual(gif.n_frames, n_frames)

    def setUp(self):
        """Run before the test."""
        # Create a GIF image
        self.gif = patch_image(create_gif_from_frames([
            Image.new('RGB', (1280, 1024), color)
            for color in ['blue', 'yellow', 'red', 'black', 'white']
        ]))

        self.check_gif(self.gif)

    def test_save(self):
        tmp_file = BytesIO()
        self.gif.save(tmp_file, 'gif')
        self.check_gif(Image.open(tmp_file))

    def test_resize(self):
        """Test resize operation on GIF image."""
        resized = self.gif.resize((100, 100))
        self.check_gif(resized, size=(100, 100))

    def test_crop(self):
        """Test crop operation on GIF image."""
        cropped = self.gif.crop((20, 20, 400, 300))
        self.check_gif(cropped, size=(380, 280))

    def test_transpose(self):
        """Test transpose operation on GIF image."""
        transposed = self.gif.transpose(Image.ROTATE_90)
        self.check_gif(transposed, size=(1024, 1280))

    def test_rotate(self):
        """Test rotate operation on GIF image."""
        rotated = self.gif.rotate(90)
        self.check_gif(rotated)  # size will not change on GIF images
