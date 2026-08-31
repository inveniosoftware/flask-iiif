# SPDX-FileCopyrightText: 2014, 2015, 2016 CERN.
# SPDX-FileCopyrightText: 2020 data-futures.
# SPDX-License-Identifier: BSD-3-Clause

"""Multimedia Image API Tests."""

from io import BytesIO

import pytest
from PIL import Image

from flask_iiif.api import IIIFImageAPIWrapper, MultimediaImage
from flask_iiif.errors import IIIFValidatorError

from .helpers import IIIFTestCase


class TestMultimediaAPI(IIIFTestCase):
    """Multimedia Image API test case."""

    @pytest.mark.parametrize(
        "width, height",
        [(1280, 1024), (100, 100), (1024, 1280), (200, 100), (1280, 720)],  # portrait
    )
    def setUp(self, width=1280, height=1024):
        """Run before the test."""
        # Create an image in memory

        tmp_file = BytesIO()
        # create a new image
        image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        image.save(tmp_file, "png")
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
        image.save(tmp_file, "jpeg")
        tmp_file.seek(0)
        self.image_not_rgba = MultimediaImage.from_string(tmp_file)

        # Image in P Mode
        tmp_file = BytesIO()
        image = Image.new("P", (width, height))
        image.save(tmp_file, "gif")
        tmp_file.seek(0)
        self.image_p_mode = MultimediaImage.from_string(tmp_file)

        # TIFF Image
        tmp_file = BytesIO()
        image = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        image.save(tmp_file, "tiff")
        tmp_file.seek(0)
        self.image_tiff = MultimediaImage.from_string(tmp_file)

    def test_image_resize(self):
        """Test image resize function."""
        # Test image size before
        self.assertEqual(str(self.image_resize.size()), str((self.width, self.height)))

        # Resize.image_resize to 720,680
        self.image_resize.resize("720,680")
        self.assertEqual(str(self.image_resize.size()), str((720, 680)))

        # Resize.image_resize to 300,
        self.image_resize.resize("300,")
        self.assertEqual(str(self.image_resize.size()), str((300, 283)))

        # Resize.image_resize to ,300
        self.image_resize.resize(",300")
        self.assertEqual(str(self.image_resize.size()), str((318, 300)))

        # Resize.image_resize to pct:90
        self.image_resize.resize("pct:90")
        self.assertEqual(str(self.image_resize.size()), str((286, 270)))

        # Resize.image_resize to !100,100
        self.image_resize.resize("!100,100")
        self.assertEqual(str(self.image_resize.size()), str((100, 94)))

    def test_errors(self):
        """Test errors."""
        from flask_iiif.errors import (
            MultimediaImageCropError,
            MultimediaImageFormatError,
            MultimediaImageNotFound,
            MultimediaImageQualityError,
            MultimediaImageResizeError,
        )

        # Test resize errors
        self.assertRaises(
            MultimediaImageResizeError, self.image_errors.resize, "pct:-12222"
        )
        self.assertRaises(MultimediaImageResizeError, self.image_errors.resize, "2")
        self.assertRaises(
            MultimediaImageResizeError, self.image_errors.resize, "-22,100"
        )
        # Test crop errors
        self.assertRaises(
            MultimediaImageCropError, self.image_errors.crop, "22,100,222"
        )
        self.assertRaises(
            MultimediaImageCropError, self.image_errors.crop, "-22,100,222,323"
        )
        self.assertRaises(
            MultimediaImageCropError, self.image_errors.crop, "pct:222,100,222,323"
        )
        self.assertRaises(
            MultimediaImageCropError, self.image_errors.crop, "2000,2000,2000,2000"
        )
        self.assertRaises(
            MultimediaImageNotFound, self.image_errors.from_file, "unicorn"
        )
        with self.app.app_context():
            self.assertRaises(
                MultimediaImageQualityError,
                self.image_errors.quality,
                "pct:222,100,222,323",
            )
            self.assertRaises(
                MultimediaImageFormatError,
                self.image_errors._prepare_for_output,
                "pct:222,100,222,323",
            )

    def test_image_crop(self):
        """Test the crop function."""
        # Crop image x,y,w,h
        self.image_crop.crop("20,20,400,300")
        self.assertEqual(str(self.image_crop.size()), str((400, 300)))

        # Crop image pct:x,y,w,h
        self.image_crop.crop("pct:20,20,40,30")
        self.assertEqual(str(self.image_crop.size()), str((160, 90)))

        # Check if exeeds image borders
        self.image_crop.crop("10,10,160,90")
        self.assertEqual(str(self.image_crop.size()), str((150, 80)))

    def test_image_rotate(self):
        """Test image rotate function."""
        self.image_rotate.rotate(90)
        self.assertEqual(str(self.image_rotate.size()), str((1024, 1280)))

        self.image_rotate.rotate(120)
        self.assertEqual(str(self.image_rotate.size()), str((1622, 1528)))

    def test_image_mode(self):
        """Test image mode."""
        self.image_not_rgba.quality("grey")
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
        self.assertEqual(self.image_tiff.image.format, "TIFF")


class TestIIIFImageAPIValidation(IIIFTestCase):
    """Validation test case for `IIIFImageAPIWrapper.validate_api`."""

    def valid_kwargs(self, version="v2", **overrides):
        """Build a known-good set of API arguments."""
        kwargs = dict(
            version=version,
            region="full",
            size="full",
            rotation="0",
            quality="native" if version == "v1" else "default",
            image_format="png",
        )
        kwargs.update(overrides)
        return kwargs

    def test_validation_rejects_trailing_and_leading_junk(self):
        """A parameter is validated over its whole length, not just a substring.

        Each of these embeds a valid token in a longer string, so an unanchored
        search accepts them even though the whole value is not a valid IIIF
        parameter.
        """
        cases = [
            ("quality", "XXXcolorYYY"),
            ("quality", "../../etc/passwd#color"),
            ("image_format", "evil.png.exe"),
            ("region", "junk1,2,3,4junk"),
            ("size", "junk100,junk"),
        ]
        for key, value in cases:
            with pytest.raises(IIIFValidatorError):
                IIIFImageAPIWrapper.validate_api(**self.valid_kwargs(**{key: value}))

    def test_validation_accepts_valid_values(self):
        """Every value valid under the IIIF Image API keeps validating."""
        cases = [
            ("v1", "region", "full"),
            ("v1", "region", "0,0,100,100"),
            ("v1", "region", "pct:10,10,50,50"),
            ("v2", "region", "full"),
            ("v2", "region", "0,0,100,100"),
            ("v2", "region", "pct:10,10,50,50"),
            ("v2", "size", "full"),
            ("v2", "size", "100,"),
            ("v2", "size", ",100"),
            ("v2", "size", "pct:50"),
            ("v2", "size", "100,200"),
            ("v2", "size", "!100,200"),
            ("v1", "rotation", "90"),
            ("v2", "rotation", "90"),
            ("v2", "rotation", "!90"),
            ("v1", "quality", "native"),
            ("v2", "quality", "default"),
            ("v2", "quality", "color"),
            ("v2", "quality", "gray"),
            ("v2", "quality", "grey"),
            ("v2", "quality", "bitonal"),
            ("v2", "image_format", "gif"),
            ("v2", "image_format", "jp2"),
            ("v2", "image_format", "jpg"),
            ("v2", "image_format", "jpeg"),
            ("v2", "image_format", "pdf"),
            ("v2", "image_format", "png"),
            ("v2", "image_format", "tif"),
            ("v2", "image_format", "tiff"),
            ("v2", "image_format", "webp"),
        ]
        for version, key, value in cases:
            kwargs = self.valid_kwargs(version=version, **{key: value})
            IIIFImageAPIWrapper.validate_api(**kwargs)
