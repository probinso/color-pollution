#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import scipy.misc as misc
import numpy as np
import imghdr

import argparse, argcomplete
import os.path as osp
import sys


def np_one_color((keep_index, img)):
  """
    takes in an image as an HxWxC and an index in range(C.len()) to preserve
    then returns the image only preserving that color.
  """
  new = np.zeros(shape=img.shape)
  new[:,:,keep_index] = img[:,:,keep_index]
  return new


def image_split(filename, dst):
  """
    split image to RBG and then saves them to dst directory
    uses process pool to speed up function
  """
  img_type   = imghdr.what(filename)
  name, suffix = osp.basename(filename).split('.')
  src_image  = misc.imread(filename)

  np_lst = enumerate([src_image]*src_image.shape[2])

  [r_image, g_image, b_image] = map(np_one_color, np_lst)

  misc.imsave(osp.join(dst, "r_" +name+ "." + img_type), r_image)
  misc.imsave(osp.join(dst, "b_" +name+ "." + img_type), b_image)
  misc.imsave(osp.join(dst, "g_" +name+ "." + img_type), g_image)


def image_split_cli(arguments):
  """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
  """
  filename  = arguments.image_filename
  directory = arguments.dst_directory
  image_split(filename, directory)


def generate_parser(parser):
  """
    helper function that generates the parser for this command
  """
  parser.add_argument('image_filename', type=str,
    help="Image Filename to be split into R, G, B images")

  parser.add_argument('dst_directory', type=str,
    help="Location to save R, G, B images")

  parser.set_defaults(func=image_split_cli)


def main():
  parser = argparse.ArgumentParser()
  generate_parser(parser)
  argcomplete.autocomplete(parser)
  arguments = parser.parse_args()
  sys.exit(arguments.func(arguments))


if __name__ == "__main__":
  main()
