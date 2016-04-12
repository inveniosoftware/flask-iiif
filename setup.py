# -*- coding: utf-8 -*-
#
# This file is part of Flask-IIIF
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
#
# Flask-IIIF is free software; you can redistribute it and/or modify
# it under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""Flask-IIIF extension provides easy IIIF API standard integration."""

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """PyTest Test."""

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        """Init pytest."""
        TestCommand.initialize_options(self)
        self.pytest_args = []
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        config = ConfigParser()
        config.read('pytest.ini')
        self.pytest_args = config.get('pytest', 'addopts').split(' ')

    def finalize_options(self):
        """Finalize pytest."""
        TestCommand.finalize_options(self)
        if hasattr(self, '_test_args'):
            self.test_suite = ''
        else:
            self.test_args = []
            self.test_suite = True

    def run_tests(self):
        """Run tests."""
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('flask_iiif', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

tests_require = [
    'flask-testing>=0.4.1',
    'check-manifest>=0.25',
    'coverage>=3.7,<4.0',
    'isort>=4.2.2',
    'pydocstyle>=2.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.6.1',
]

install_requires = [
    'Flask>=0.10.1',
    'Flask-RESTful>=0.2.12',
    'blinker>=1.4',
    'six>=1.7.2',
    'pillow>=3.4',
]

extra_require = {
    'docs': [
        'Sphinx>=1.4.2',
    ],
    'redis': [
        'redis>=2.10.5',
    ],
    'tests': tests_require,
}

extra_require['all'] = []
for reqs in extra_require.values():
    extra_require['all'].extend(reqs)

setup(
    name='Flask-IIIF',
    version=version,
    url='http://github.com/inveniosoftware/flask-iiif/',
    license='BSD',
    author='Invenio collaboration',
    author_email='info@inveniosoftware.org',
    description=__doc__,
    long_description=open('README.rst').read(),
    packages=['flask_iiif'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    extras_require=extra_require,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 5 - Production/Stable',
    ],
)
