#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

from   collections import defaultdict
from   itertools   import tee
import os.path as osp
import sys

import ddbscan
import imghdr
import matplotlib.pyplot as plt
import numpy   as np
import scipy.misc as misc

from utility import take, ptrace

"""
Lamplight Module

This module houses interesting operations on images for lamplight analysis
"""


@ptrace
def image_info(filename):
    """
    Takes in a filename
    returns a tuple (filetype, basename(filename), numpy image)
    """
    img_type   = imghdr.what(filename)
    name, suffix = osp.basename(filename).rsplit('.', 1)
    src_image  = misc.imread(filename)
    return img_type, name, src_image


@ptrace
def save_images(dst, name, img_type, **kwargs):
    """
    input:
      dst  is a directory destination
      name is the expected name of the image to be saved
      img_type is the saving filetype
      kwargs is dictionary of numpy image arrays
    output:
      saves images into dst with name
    """
    @ptrace
    def save_modified(prefix, image):
        result = osp.join(dst, prefix + name + "." + img_type)
        misc.imsave(result, image)
        return result

    for i in kwargs:
        save_modified(i, kwargs[i])


@ptrace
def image_split(src_image, channels=3):
    """
    split image to RBG and then saves them to dst directory
    uses process pool to speed up function

    we can get rid of channels by using 'Extended Iterable Unpacking'
    however this is not yet in the language
    """
    @ptrace
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
    """
    Object, probably needs documentation
    """
    def __init__(self, step=10, delta=5, maxvalue=255):
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


@ptrace
def topograph_image(image, step_gen):
    """
    Takes in NxMxC matrix and a step size and a delta
    returns NxMxC matrix with contours in each C cell
    """
    new_img = np.array(image, copy=True)

    def myfunc(color):
        for value in step_gen.range:
            tops, bots = value + step_gen.delta, value - step_gen.delta
            if (color <= tops) and (color >= bots):
                return value
            if color > tops:
                break
        return 0

    topograph = np.vectorize(myfunc)
    return topograph(new_img)


@ptrace
def get_index_of(image):
    """
    splits image into dict[channels][intensities] as (x, y) point pairs
    this is used to shrink and split the search space for clustering

    this function is much more useful if run on result of topograph_image
    """
    ret = defaultdict(lambda : defaultdict(list))
    for x, column in enumerate(image):
        for y, pixel in enumerate(column):
            for channel, intensity in enumerate(pixel):
                ret[channel][intensity].append([x,y])
    return ret


@ptrace
def make_clusters_dict(points_dict, step_gen, radius=5, minpoints=10):
    """
    Input:
      points_dict - dictionary of points indexed by d[band][intensity]
      step_gen    - valid band generator
      radius      - size of radius for ddbscan algorithm
      minpoints   - minimal number of points to be called a cluster
    Output:
      dictionary[band][intensity][cluster_id] = [[x, y]]
    """
    @ptrace
    def make_clusters(points, radius, minpoints):
        """
        Takes in a list of [x, y] points
        returns a dict of lists of points
        """
        scan = ddbscan.DDBSCAN(radius, minpoints)
        for p in points:
            scan.add_point(p, count=1, desc="")

        scan.compute()

        """
        for index, cluster in enumerate(scan.clusters):
            print '=== Cluster %d ===' % index
            print 'Cluster points index: %s' % len(list(cluster))
        """

        d = defaultdict(list)
        for i, p in enumerate(scan.points):
            if scan.points_data[i].cluster == -1:
                # cluster_id == -1 is an anomolous point
                continue
            d[scan.points_data[i].cluster].append(p)

        return d

    retval = defaultdict(lambda : defaultdict(list))
    for l_intensity in take(step_gen.range, 1) if True else step_gen.range:
        for l_channel in points_dict:
            retval[l_channel][l_intensity] = \
              make_clusters(points_dict[l_channel][l_intensity], radius, minpoints)

    return retval


@ptrace
def colorize_clusters(base_img, clusters):
    """
    Input base_img numpy array, and dictionary of clusters
    Outputs a copy of base_img with identified clusters filled with colors
    """
    new_img = np.array(base_img, copy=True)
    colors = plt.cm.Spectral(np.linspace(0 , 1, len(clusters)))*255

    for i, c in enumerate(clusters):
        for [x, y] in clusters[c]:
            new_img[x, y] = colors[i][:3]
    return new_img
