#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

import sys
if sys.version_info.major < 3:
    print("I'm only for 3, please upgrade")
    sys.exit(1)

here = path.abspath(path.dirname(__file__))

setup(
  name         = 'lamplibs',
  version      = '0.0.0',
  description  = 'Colour Pollution Course',
  author       = 'Philip Robinson',
  author_email = 'pmoss.robinson@gmail.com',
  license      = 'BEERWARE',

  classifiers  = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
    'License :: BEERWARE',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    ],

  url          = 'https://www.github.com/color-polution',
  packages     = find_packages(exclude=[]),
  entry_points = { # enable cmd-line access
    "console_scripts": [
      'lamp = lamplibs.lamp:main',
    ]
    },
  scripts = [],
  package_data={}, #{'peval': ['db_init.sql']},
  data_files=[(os.path.join('share','%s','%s') % ('lamplibs', x[0]), map(lambda y: x[0]+ os.path.sep +y, x[2])) for x in os.walk('images'+os.path.sep)],
  long_description=read('README.md'),
  install_requires = [
    'appdirs',
    'argcomplete',
    'argparse',
    'matplotlib',
    'numpy',
    'scipy',
    'imread',
    'Pillow',
    'scikit-learn',
    'pony',
  ]
)

