#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import numpy as np
from extractRGB import image_info, image_split, save_images
import argparse, argcomplete
import os.path as osp
import sys


def topograph_image(image, step=30, delta=5):
  """
    Takes in NxMxC matrix and a step size and a delta
    returns NxMxC matrix with contours in each C cell
  """

  def myfunc(color, maxvalue=255):
    for value in range(step, maxvalue, step):
      tops, bots = value + delta, value - delta
      if color < bots:
        break
      if (color < tops) and (color > bots):
        return value
    return 0
  topograph = np.vectorize(myfunc)
  
  return topograph(image)


def image_split_cli(arguments):
  """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
  """
  filename  = arguments.image_filename
  directory = arguments.dst_directory
  img_type, name, src_image = image_info(filename)
  r, g, b = image_split(src_image)
  top_image = topograph_image(r+b)
  
  save_images(directory, name, img_type, top_=top_image)


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
