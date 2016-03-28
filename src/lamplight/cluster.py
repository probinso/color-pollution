#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-"""

import argparse, argcomplete
import sys

from lamplight import step_range_gen, image_info, save_images
from lamplight import topograph_image, paint_points
from lamplight import get_index_of, make_clusters_dict, overlapping_clusters

from lamplight import colorize_clusters

def select_clusters(image):
    step_gen  = step_range_gen(20)
    top_image = topograph_image(image, step_gen)

    radius, size = 3, 50

    def paint(top_img, dst_img):
        points_dict  = get_index_of(top_img)
        cluster_dict = make_clusters_dict(points_dict, step_gen, 30, 100)
        for overlapping in overlapping_clusters(cluster_dict, step_gen):
            print(overlapping)

        channel, intensity = 1, next(step_gen) # green, 255
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
