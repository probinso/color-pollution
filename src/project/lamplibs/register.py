#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import os
import os.path as osp
import sys

from   .lamplight import image_info, save_images
from   .          import model as mod
from   .utility   import commit_resource, sign_path, TemporaryDirectory


########################################
#                IMAGES
########################################
@mod.pny.db_session
def register_image_db(label, height, width, img_type, derived=True):
    img = mod.Image.get(id=label)
    if not img:
        img = mod.Image(
            id=label,
            height=height,
            width=width,
            type=img_type,
            derived=derived
        )
    return img


def register_image_data(src_image):
    with TemporaryDirectory() as tmpdir:
        [filename] = save_images(tmpdir, 'tmp', tmp_=src_image)
        return register_image_file(filename, True)


def register_image_file(filename, derived=False):
    image_type, name, dst_data = image_info(filename)
    (h, w, _d) = dst_data.shape
    label = commit_resource(filename)

    return register_image_db(label, h, w, image_type, derived)


def interface(filename):
    img = register_image_file(filename)
    register_image_data(img.data)


def cli_interface(arguments):
    filename = arguments.image_filename
    interface(filename)


def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image filename to register")
    parser.set_defaults(func=cli_interface)
    return parser
