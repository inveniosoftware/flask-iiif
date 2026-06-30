#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2014-2024 CERN.
# SPDX-FileCopyrightText: 2022 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
function cleanup() {
    eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT

# TODO: We've temporarily removed the -W flag because of unresolvable warnings
python -m sphinx.cmd.build -qnN docs docs/_build/html
eval "$(docker-services-cli up --cache ${CACHE:-redis} --env)"
python -m pytest
tests_exit_code=$?
exit "$tests_exit_code"
