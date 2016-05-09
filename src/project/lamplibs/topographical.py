#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import sys

from .lamplight import image_info, save_images
from .lamplight import topograph_image
from .utility   import sign_path

from .register  import register_image_file, register_image_data
from .          import model as mod

@mod.pny.db_session
def register_topograph_db(src_image, dst_image, step):
    top = mod.Topograph.get(dst_image=dst_image, step=step, src_image=src_image)
    if not top:
        top = mod.Topograph(
            dst_image=dst_image,
            step=step,
            src_image=src_image
        )
    return top


@mod.pny.db_session
def check_topograph(src, step):
    src_image = register_image_file(src)
    top = mod.Topograph.get(step=step, src_image=src_image)
    if not top:
        top_data  = topograph_image(src_image.data, step)
        top_image = register_image_data(top_data)
        top       = register_topograph_db(src_image, top_image, step)

    return top.dst_image.id


def interface(filename, directory, step):
    resource = check_topograph(filename, step)
    mod.retrieve_image(resource, directory)


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename  = arguments.image_filename
    directory = arguments.dst_directory
    step      = arguments.step
    interface(filename, directory, step)


#####################################
##         PARSERS
#####################################

def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image Filename to topograph")
    parser.add_argument('dst_directory', type=str,
        help="Location to save modified images")
    parser.add_argument('--step', type=int, default=10,
        help="step size for topographing an image.")
    parser.set_defaults(func=cli_interface)
    return parser


