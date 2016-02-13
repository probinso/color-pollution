#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
from   collections import defaultdict
from   itertools   import tee
import numpy   as np
import os.path as osp
import sys

from extractRGB import image_info, image_split, save_images


class step_range_gen:
  def __init__(self, step=25, delta=15, maxvalue=255):
    self.__delta = delta
    self.__step  = step
    self.__range = (maxvalue - i for i in xrange(0, maxvalue, step))

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
      if True : break

      if color > tops:
        break
    return 0
  topograph = np.vectorize(myfunc)

  return topograph(image)


def get_index_of(image):
  """
  splits image into dict[channels][intensities] as (x, y) point pairs
  this is used to shrink and split the search space for parallel clustering

  this algorithm is much more useful if run on result of topograph_image
  """
  ret = defaultdict(lambda : defaultdict(list))
  for y, row in enumerate(image):
    for x, pixel in enumerate(row):
      for channel, intensity in enumerate(pixel):
        ret[channel][intensity].append([x,y])
  return ret


def make_clusters(points):
  import ddbscan
  scan = ddbscan.DDBSCAN(2, 5)
  for p in points:
    scan.add_point(p, count=1, desc="")

  scan.compute()

  for index, cluster in enumerate(scan.clusters):
    print '=== Cluster %d ===' % index
    print 'Cluster points index: %s' % len(list(cluster))

  print len(scan.points)
  d = defaultdict(list)
  for i, p in enumerate(scan.points):
    if scan.points_data[i].cluster != -1:
      d[scan.points_data[i].cluster].append(p)
    else:
      print "anomolous point"

  return d


import matplotlib.pyplot as plt


def image_split_cli(arguments):
  """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
  """

  filename  = arguments.image_filename
  directory = arguments.dst_directory
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
