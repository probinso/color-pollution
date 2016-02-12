#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import numpy as np
from extractRGB import image_info, image_split, save_images
from itertools import tee
import argparse, argcomplete
import os.path as osp
import sys
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


class step_range_gen:
  def __init__(self, step=8, delta=4, maxvalue=255):
    self.__delta = delta
    self.__step  = step
    self.__range = (maxvalue - delta - i for i in xrange(0, maxvalue, step))

  @property
  def delta(self):
    return self.__delta

  @property
  def range(self):
    local, self.__range = tee(self.__range)
    for i in local:
      yield i

def topograph_image(image, step_gen):
  """
    Takes in NxMxC matrix and a step size and a delta
    returns NxMxC matrix with contours in each C cell
  """

  def myfunc(color):
    for value in step_gen.range:
      tops, bots = value + step_gen.delta, value - step_gen.delta
      if (color <= tops) and (color >= bots):
        return value
      if color > tops:
        break
    return 0
  topograph = np.vectorize(myfunc)

  return topograph(image)


def get_index_of(image, step_gen):
  from collections import defaultdict
  ret = defaultdict(lambda : defaultdict(lambda : np.ndarray((0, 2))))
  for target_color in step_gen.range:
    for y, row in enumerate(image):
      for x, pixel in enumerate(row):
        for c, value in enumerate(pixel):
          if value == target_color:
            ret[c][target_color] = np.append(ret[c][target_color], [[x, y]], axis=0)
  return ret


"""
##############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
"""

def image_split_cli(arguments):
  """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
  """

  filename  = arguments.image_filename
  directory = arguments.dst_directory
  img_type, name, src_image = image_info(filename)

  step_gen = step_range_gen()

  top_image = src_image if True else topograph_image(src_image, step_gen)
  points_dict = get_index_of(top_image, step_gen)

  #save_images(directory, name, img_type, top_=top_image)


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
