#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-"""

import argparse, argcomplete
import sys

from .lamplight import step_range_gen, image_info, save_images
from .lamplight import topograph_image
from .lamplight import get_index_of, make_clusters_dict, overlapping_clusters, simplexify
from .lamplight import colorize_clusters


def select_clusters(image):
    step_gen  = step_range_gen(10)
    top_image = topograph_image(image, step_gen)

    radius, size = 30, 5

    def paint(top_img, dst_img):
        points_dict  = get_index_of(top_img, step_gen)
        cluster_dict = make_clusters_dict(points_dict, step_gen, radius, size)
        for overlapping in overlapping_clusters(cluster_dict, step_gen):
            print(simplexify(overlapping), file=sys.stdout)

        channel, intensity = 2, next(step_gen) # blue, 255
        clusters = cluster_dict[channel, intensity]

        return colorize_clusters(dst_img, clusters)

    save_top = paint(top_image, image)
    return save_top


def interface(filename, directory):
    img_type, name, src_image = image_info(filename)
    new_image = select_clusters(src_image)
    save_images(directory, name, img_type, top_=new_image)


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
