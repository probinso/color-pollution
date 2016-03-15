#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import sys

from lamplight import image_info, save_images, image_split
from lamplight import step_range_gen, topograph_image
from lamplight import get_index_of, make_clusters_dict, colorize_clusters


def interface(filename, directory):
    img_type, name, src_image = image_info(filename)
    step_gen  = step_range_gen(20)

    top_image = topograph_image(src_image, step_gen)

    save_images(directory, name, img_type ,top_=top_image)


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
