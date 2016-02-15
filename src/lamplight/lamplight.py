#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

from   collections import defaultdict
from   itertools   import tee
import os.path as osp
import sys

import ddbscan
import imghdr
import numpy   as np
import scipy.misc as misc

"""Lamplight Module

This module houses interesting operations on images for lamplight analysis
"""


def image_info(filename):
  """
    Takes in a filename
    returns a tuple (filetype, basename(filename), numpy image
  """
  img_type   = imghdr.what(filename)
  name, suffix = osp.basename(filename).rsplit('.', 1)
  src_image  = misc.imread(filename)
  return img_type, name, src_image


def save_images(dst, name, img_type, **kwargs):
  """
    input:
      dst  is a directory destination
      name is the expected name of the image to be saved
      img_type is the saving filetype
      kwargs   is denotes is a numpy
    output:
      saves images into dst with name
  """
  def save_modified(prefix, image):
    name = osp.join(dst, prefix + name + "." + img_type)
    misc.imsave(name, image)

  for i in kwargs:
    save_modified(i, kwargs[i])


def image_split(src_image, channels=3):
  """
  split image to RBG and then saves them to dst directory
  uses process pool to speed up function

  we can get rid of channels by using 'Extended Iterable Unpacking'
  however this is not yet in the language
  """

  def np_one_color((keep_index, img)):
    """
    input image as an HxWxC numpy.array an index in range(C.len()) to preserve
    returns the image only preserving that color.
    """
    new = np.zeros(shape=img.shape)
    new[:,:,keep_index] = img[:,:,keep_index]
    return new

  np_lst = enumerate([src_image]*src_image.shape[2])
  return map(np_one_color, np_lst)[:channels]


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




