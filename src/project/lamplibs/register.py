# -*- coding: utf-8 -*-"""
"""
This module registers images to the database, The CLI to this operation has
been depricated.
"""

import argparse, argcomplete
import os
import os.path as osp
import sys

from   .lamplight import image_info, save_images
from   .          import model as mod
from   .utility   import TemporaryDirectory


########################################
#                IMAGES
########################################
def commit_register_image_data(src_image):
    with TemporaryDirectory() as tmpdir:
        [filename] = save_images(tmpdir, 'tmp', tmp_=src_image)
        label = mod.commit_resource(filename)
    return _register_image_file(label)


def commit_register_image_file(filename):
    label = mod.commit_resource(filename)
    return _register_image_file(label)


@mod.check_tables(mod.Image)
def _register_image_file(label):
    image_type, name, dst_data = image_info(mod.get_resource(label))
    (h, w, _d) = dst_data.shape
    return {'label':label, 'height':h, 'width':w, 'img_type':image_type}


def cli_interface(arguments):
    filename = arguments.image_filename
    _ = commit_register_image_file(filename)


def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image filename to register")
    parser.set_defaults(func=cli_interface)
    return parser
