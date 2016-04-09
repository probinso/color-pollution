#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import sys

from .lamplight import image_info, save_images
from .lamplight import step_range_gen, topograph_image


def interface(filename, directory, step):
    img_type, name, src_image = image_info(filename)
    step_gen  = step_range_gen(10)

    top_image = topograph_image(src_image, step_gen)

    save_images(directory, name,top_=top_image)


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


