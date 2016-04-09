#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-"""

import argparse, argcomplete
import sys

from .lamplight import step_range_gen, image_info, save_images, empty_canvas
from .lamplight import get_index_of, make_clusters_dict, overlapping_clusters, simplexify
from .lamplight import colorize_clusters


def select_clusters(image):
    step_gen = step_range_gen(30)
    radius, size = 30, 20

    def paint(src_img, dst_img):
        points_dict  = get_index_of(src_img, step_gen)
        cluster_dict = make_clusters_dict(points_dict, step_gen, radius, size)

        order = lambda o: len(o[1])
        for overlapping in overlapping_clusters(cluster_dict, step_gen):
            print(simplexify(overlapping), file=sys.stdout)
            for key, clstr in sorted(overlapping.items(), key=order, reverse=True):
                col      = [0, 0, 0]
                col[key] = 255
                dst_img = colorize_clusters(dst_img, col, clstr)

        return dst_img

    dst_img  = empty_canvas(image)
    save_img = paint(image, dst_img)

    return save_img


def interface(filename, directory):
    img_type, name, src_image = image_info(filename)
    new_image = select_clusters(src_image)
    save_images(directory, name, clst_=new_image)


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename  = arguments.image_filename
    directory = arguments.dst_directory
    interface(filename, directory)


#####################################
##         PARSERS
#####################################
def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image Filename to be split into R, G, B images")
    parser.add_argument('dst_directory', type=str,
        help="Location to save modified images")
    parser.set_defaults(func=cli_interface)
    return parser
