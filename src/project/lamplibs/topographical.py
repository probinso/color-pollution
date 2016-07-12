# -*- coding: utf-8 -*-"""
"""
This module provides operational support of data smoothing over images.
"""

import argparse, argcomplete
import sys

from .lamplight import image_info, save_images
from .lamplight import topograph_image
from .utility   import sign_path, ptrace

from .register  import commit_register_image_data, commit_register_image_file
from .          import model as mod


@mod.check_tables(mod.Topograph)
def check_topograph(src_image, step):
    top_data  = topograph_image(src_image.data, step)
    top_image = commit_register_image_data(top_data)
    return {'dst_image':top_image, 'src_image':src_image, 'step':step}


def interface(filename, directory, step):
    src_image = commit_register_image_file(filename)
    resource  = check_topograph(src_image, step)
    mod.retrieve_image(resource.dst_image.label, directory)


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


