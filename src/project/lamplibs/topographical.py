#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import sys

from .lamplight import image_info, save_images
from .lamplight import step_range_gen, topograph_image
from .utility   import sign_path

from .register  import register_image_file, register_image_data
from .          import model as mod

@mod.pny.db_session
def register_topograph_db(src_img, dst_img, step):
    top = mod.Topograph.get(dst_image=dst_img, step=step, src_image=src_img)
    if not top:
        top = mod.Topograph(
            dst_image=dst_img,
            step=step,
            src_image=src_img
        )
    return top.dst_image

@mod.pny.db_session
def check_topograph(src, step):
    s_img_type, suid, src_data = register_image_file(src)
    src_img = mod.Image.get(id=suid)
    top = mod.Topograph.get(step=step, src_image=src_img)
    if top:
        resource = top.dst_image.id
    else:
        step_gen  = step_range_gen(step)
        top_image = topograph_image(src_data, step_gen)
        _d_img_type, duid, _dst_data = register_image_data(top_image)
        resource = register_topograph_db(suid, duid, step).id
    return resource


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


