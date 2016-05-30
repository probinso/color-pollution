# -*- coding: utf-8 -*-"""
"""
This module provides a simple CLI for extracting Red-Green-Blue from images
"""
import argparse, argcomplete
import os.path as osp
import sys

from .lamplight import image_info, image_split, save_images

def interface(filename, directory):
    img_type, name, src_image     = image_info(filename)
    r_image, g_image, b_image, *alpha = image_split(src_image)
    if alpha: # handle alphas for .png file extension
        r_image = r_image + alpha[0]
        g_image = g_image + alpha[0]
        b_image = b_image + alpha[0]

    save_images(directory, name, r_=r_image, b_=b_image, g_=g_image)


def cli_interface(arguments):
    """
      by convention it is helpful to have a wrapper_cli method that interfaces
      from commandline to function space.
    """
    filename  = arguments.image_filename
    directory = arguments.dst_directory
    interface(filename, directory)


def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
      help="Image Filename to be split into R, G, B images")

    parser.add_argument('dst_directory', type=str,
      help="Location to save modified images")

    parser.set_defaults(func=cli_interface)
    return parser
