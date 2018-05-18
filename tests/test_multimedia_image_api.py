# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Multimedia Image API Tests."""

from io import BytesIO

import pytest
from PIL import Image

from flask_iiif.api import MultimediaImage
from flask_iiif.utils import create_gif_from_frames

from .helpers import IIIFTestCase


class TestMultimediaAPI(IIIFTestCase):
    """Multimedia Image API test case."""

    @pytest.mark.parametrize("width, height",
                             [(1280, 1024),
                              (100, 100),
                              (1024, 1280),  # portrait
                              (200, 100),
                              (1280, 720),
                              ])
    def setUp(self, width=1280, height=1024):
        """Run before the test."""
        # Create an image in memory

        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        image.save(tmp_file, 'png')

        # create a new gif image
        self.image_gif = MultimediaImage(create_gif_from_frames([
            Image.new("RGB", (width, height), color)
            for color in ['blue', 'yellow', 'red', 'black', 'white']
        ]))
        self.width, self.height = width, height
        # Initialize it for our object and create and instance for
        # each test
        tmp_file.seek(0)
        self.image_resize = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_crop = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_rotate = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_errors = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_convert = MultimediaImage.from_string(tmp_file)
        tmp_file.seek(0)
        self.image_save = MultimediaImage.from_string(tmp_file)

        # NOT RGBA
        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGB", (width, height), (255, 0, 0, 0))
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        self.image_not_rgba = MultimediaImage.from_string(tmp_file)

        # Image in P Mode
        tmp_file = BytesIO()
        image = Image.new("P", (width, height))
        image.save(tmp_file, 'gif')
        tmp_file.seek(0)
        self.image_p_mode = MultimediaImage.from_string(tmp_file)

        # TIFF Image
        tmp_file = BytesIO()
        image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        image.save(tmp_file, 'tiff')
        tmp_file.seek(0)
        self.image_tiff = MultimediaImage.from_string(tmp_file)

    def test_gif_resize(self):
        """Test image resize function on GIF images."""
        # Check original size and GIF properties
        self.assertEqual(self.image_gif.image.is_animated, True)
        self.assertEqual(self.image_gif.image.n_frames, 5)
        self.assertEqual(str(self.image_gif.size()),
                         str((self.width, self.height)))

        # Assert proper resize and preservation of GIF properties
        self.image_gif.resize('720,680')
        self.assertEqual(self.image_gif.image.is_animated, True)
        self.assertEqual(self.image_gif.image.n_frames, 5)
        self.assertEqual(str(self.image_gif.size()), str((720, 680)))

        # test gif resize best fit
        self.image_gif.resize('!400,220')
        self.assertEqual(self.image_gif.image.is_animated, True)
        self.assertEqual(self.image_gif.image.n_frames, 5)
        self.assertEqual(str(self.image_gif.size()), str((400, 220)))

    def test_image_resize(self):
        """Test image resize function."""
        # Test image size before
        self.assertEqual(str(self.image_resize.size()),
                         str((self.width, self.height)))

        # Resize.image_resize to 720,680
        self.image_resize.resize('720,680')
        self.assertEqual(str(self.image_resize.size()), str((720, 680)))

        # Resize.image_resize to 300,
        self.image_resize.resize('300,')
        self.assertEqual(str(self.image_resize.size()), str((300, 283)))

        # Resize.image_resize to ,300
        self.image_resize.resize(',300')
        self.assertEqual(str(self.image_resize.size()), str((318, 300)))

        # Resize.image_resize to pct:90
        self.image_resize.resize('pct:90')
        self.assertEqual(str(self.image_resize.size()), str((286, 270)))

        # Resize.image_resize to !100,100
        self.image_resize.resize('!100,100')
        self.assertEqual(str(self.image_resize.size()), str((100, 100)))

    def test_errors(self):
        """Test errors."""
        from flask_iiif.errors import (
            MultimediaImageResizeError, MultimediaImageCropError,
            MultimediaImageNotFound, MultimediaImageQualityError,
            MultimediaImageFormatError
        )
        # Test resize errors
        self.assertRaises(
            MultimediaImageResizeError,
            self.image_errors.resize,
            'pct:-12222'
        )
        self.assertRaises(
            MultimediaImageResizeError,
            self.image_errors.resize,
            '2'
        )
        self.assertRaises(
            MultimediaImageResizeError,
            self.image_errors.resize,
            '-22,100'
        )
        # Test crop errors
        self.assertRaises(
            MultimediaImageCropError,
            self.image_errors.crop,
            '22,100,222'
        )
        self.assertRaises(
            MultimediaImageCropError,
            self.image_errors.crop,
            '-22,100,222,323'
        )
        self.assertRaises(
            MultimediaImageCropError,
            self.image_errors.crop,
            'pct:222,100,222,323'
        )
        self.assertRaises(
            MultimediaImageCropError,
            self.image_errors.crop,
            '2000,2000,2000,2000'
        )
        self.assertRaises(
            MultimediaImageNotFound,
            self.image_errors.from_file,
            "unicorn"
        )
        with self.app.app_context():
            self.assertRaises(
                MultimediaImageQualityError,
                self.image_errors.quality,
                'pct:222,100,222,323'
            )
            self.assertRaises(
                MultimediaImageFormatError,
                self.image_errors._prepare_for_output,
                'pct:222,100,222,323'
            )

    def test_image_crop(self):
        """Test the crop function."""
        # Crop image x,y,w,h
        self.image_crop.crop('20,20,400,300')
        self.assertEqual(str(self.image_crop.size()), str((400, 300)))

        # Crop image pct:x,y,w,h
        self.image_crop.crop('pct:20,20,40,30')
        self.assertEqual(str(self.image_crop.size()), str((160, 90)))

        # Check if exeeds image borders
        self.image_crop.crop('10,10,160,90')
        self.assertEqual(str(self.image_crop.size()), str((150, 80)))

    def test_image_rotate(self):
        """Test image rotate function."""
        self.image_rotate.rotate(90)
        self.assertEqual(str(self.image_rotate.size()), str((1024, 1280)))

        self.image_rotate.rotate(120)
        self.assertEqual(str(self.image_rotate.size()), str((1024, 1280)))

    def test_image_mode(self):
        """Test image mode."""
        self.image_not_rgba.quality('grey')
        self.assertEqual(self.image_not_rgba.image.mode, "L")

    def test_image_incompatible_modes(self):
        """Test P-incompatible image to RGB auto-convert."""
        tmp_file = BytesIO()
        self.image_p_mode.save(tmp_file)
        self.assertEqual(self.image_p_mode.image.mode, "RGB")

    def test_image_saving(self):
        """Test image saving."""
        tmp_file = BytesIO()
        compare_file = BytesIO()
        self.assertEqual(tmp_file.getvalue(), compare_file.getvalue())
        self.image_save.save(tmp_file)
        self.assertNotEqual(str(tmp_file.getvalue()), compare_file.getvalue())

    def test_image_tiff_support(self):
        """Test TIFF image support."""
        self.assertEqual(self.image_tiff.image.format, 'TIFF')
