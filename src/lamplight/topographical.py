#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import os.path as osp
import sys

from lamplight import take # why this isn't part of itertools i know not.
from lamplight import image_info, save_images, image_split
from lamplight import step_range_gen, topograph_image
from lamplight import get_index_of, make_clusters_dict, colorize_clusters

from collections import defaultdict


import numpy as np # i should never have to do this


def g(image, step_gen):
    points_dict  = get_index_of(image)
    cluster_dict = make_clusters_dict(points_dict, step_gen)
    del points_dict
    clusters = cluster_dict[1][next(take(step_gen.range, 1))]
    image = colorize_clusters(image, clusters)
    del cluster_dict
    return image


def interface(filename, directory):
    img_type, name, src_image = image_info(filename)

    step_gen = step_range_gen(30, 15)

    top_image = topograph_image(src_image, step_gen)

    src_image = g(src_image, step_gen)
    top_image = g(top_image, step_gen)
    save_images(directory, name, img_type ,top_=top_image, src_=src_image)    
    

def cli_interface(arguments):
    """
        by convention it is helpful to have a wrapper_cli method that interfaces
        from commandline to function space.
    """

    filename  = arguments.image_filename
    directory = arguments.dst_directory
    interface(filename, directory)


def generate_parser(parser):
    """
        helper function that generates the parser for this command
    """
    parser.add_argument('image_filename', type=str,
        help="Image Filename to be split into R, G, B images")

    parser.add_argument('dst_directory', type=str,
        help="Location to save modified images")

    parser.set_defaults(func=cli_interface)


def main():
    parser = argparse.ArgumentParser()
    generate_parser(parser)
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()
    sys.exit(arguments.func(arguments))


if __name__ == "__main__":
    main()
