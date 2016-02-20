#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import os.path as osp
import sys

from utility   import take, fc

from lamplight import image_info, save_images, image_split
from lamplight import step_range_gen, topograph_image
from lamplight import get_index_of, make_clusters_dict, colorize_clusters
from lamplight import compute_mediod

from collections import defaultdict

def g(image, step_gen):
    points_dict  = get_index_of(image)
    cluster_dict = make_clusters_dict(points_dict, step_gen)
    images = []
    for intensity in take(step_gen.range, 3):
        for channel in [0, 1, 2]: # r, g, b
            clusters = cluster_dict[channel][intensity]
            images.append(colorize_clusters(image, clusters))
    return images[1] # green, 255


def paint(image, step_gen):
    points_dict  = get_index_of(image)
    cluster_dict = make_clusters_dict(points_dict, step_gen, 30, 100)

    channel, intensity = 1, next(step_gen.range) # green, 255
    clusters = cluster_dict[channel][intensity]
    print compute_mediod(clusters[0])

    return colorize_clusters(image, clusters)


def interface(filename, directory):
    img_type, name, src_image = image_info(filename)
    step_gen = step_range_gen(30, 15)

    top_image = topograph_image(src_image, step_gen)

    src_image, top_image = paint(top_image, step_gen), paint(src_image, step_gen)

    save_images(directory, name, img_type ,top_=top_image, src_=src_image)

    for key in fc:
        print key, fc[key]


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
