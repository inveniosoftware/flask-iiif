#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014-2024 CERN.
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
function cleanup() {
    eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT

python -m check_manifest
# TODO: We've temporarily removed the -W flag because of unresolvable warnings
python -m sphinx.cmd.build -qnN docs docs/_build/html
eval "$(docker-services-cli up --cache ${CACHE:-redis} --env)"
python -m pytest
tests_exit_code=$?
exit "$tests_exit_code"
