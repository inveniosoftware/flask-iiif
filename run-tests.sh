#!/bin/sh
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

pydocstyle flask_iiif && \
isort -c -c -df **/*.py && \
check-manifest --ignore ".travis-*" --ignore docs/_themes && \
sphinx-build -qnNW docs docs/_build/html && \
python setup.py test
