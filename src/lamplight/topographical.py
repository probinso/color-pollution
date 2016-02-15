#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
from   collections import defaultdict
from   itertools   import tee
import numpy   as np
import os.path as osp
import sys

from lamplight import image_info, save_images, image_split
from lamplight import step_range_gen
from lamplight import topograph_image, get_index_of, make_clusters


import matplotlib.pyplot as plt


def interface(filename, directory):
  img_type, name, src_image = image_info(filename)

  step_gen = step_range_gen()

  r, g, b = image_split(src_image)
  top_image = topograph_image(g, step_gen)

  points_dict = get_index_of(top_image)
  l_channel, l_intensity = 1, next(step_gen.range) # green at highest intensity
  clusters = make_clusters(points_dict[l_channel][l_intensity])

  colors   = plt.cm.Spectral(np.linspace(0 , 1, len(clusters)))*255
  for i, c in enumerate(clusters):
    for [y , x] in clusters[c]:
      top_image[x,y] = colors[i][:3]

  save_images(directory, name, img_type, top_=top_image)
  

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
