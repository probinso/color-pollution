
import os
from setuptools import setup

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name         = 'lamplibs',
  version      = '0.0',
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
  packages     = ['lamplibs'],
  entry_points = { # enable cmd-line access
    "console_scripts": [
      'lamp = lamplibs.lamp:main',
    ]
    },
  scripts = [],
  package_data={}, #{'peval': ['db_init.sql']},
  data_files=[('share/%s/%s' % ('peval', x[0]), map(lambda y: x[0]+'/'+y, x[2])) for x in os.walk('images'+osp.sep)],
  long_description=read(os.path.join('lamplibs','README.md')),
  install_requires = [
    'argcomplete',
    'argparse',
    'ddbscan',
    'matplotlib',
    'numpy',
    'scipy',
    'imread',
    'Pillow',
  ]
)

