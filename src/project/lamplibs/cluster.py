# -*- coding: utf-8 -*-"""
"""
This module administrates lamp clustering and feature extraction.
"""

import argparse, argcomplete
import sys

from .lamplight import image_info, save_images, empty_canvas
from .lamplight import get_index_cond, make_clusters_dict, overlapping_clusters, simplexify
from .lamplight import colorize_clusters


def select_clusters(image, radius, size):

    def paint(src_img, dst_img):
        points_dict  = get_index_cond(src_img)
        cluster_dict = make_clusters_dict(points_dict, radius, size)

        order = lambda o: len(o[1])
        print(len(cluster_dict))
        for i, overlapping in enumerate(overlapping_clusters(cluster_dict)):
            print("visiting cluster : {}".format(i))
            print(simplexify(overlapping), file=sys.stdout)
            for key, clstr in sorted(overlapping.items(), key=order, reverse=True):
                col      = [0, 0, 0]
                col[key] = 255
                dst_img = colorize_clusters(dst_img, col, clstr)

        return dst_img

    dst_img  = empty_canvas(image)
    save_img = paint(image, dst_img)

    return save_img


def interface(filename, directory, radius, size):
    img_type, name, src_image = image_info(filename)
    new_image = select_clusters(src_image, radius, size)
    save_images(directory, name, clst_=new_image)


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename  = arguments.image_filename
    directory = arguments.dst_directory
    radius    = arguments.radius
    size      = arguments.size
    interface(filename, directory, radius, size)


#####################################
##         PARSERS
#####################################
def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image Filename to be clustered")
    parser.add_argument('dst_directory', type=str,
        help="Location to save modified images")
    parser.add_argument('--radius', type=int, default=30,
        help="Cluster acceptance radius")
    parser.add_argument('--size', type=int, default=20,
        help="Cluster minimum size")
    parser.set_defaults(func=cli_interface)
    return parser
