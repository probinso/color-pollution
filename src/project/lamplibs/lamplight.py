#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

# Python Standard Libarary
from   collections import namedtuple, defaultdict
from   functools   import partial
from   math        import ceil
from   operator    import itemgetter
import os.path as osp
from   sys import stderr

# External Dependencies
import imghdr
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc
#from   scipy.spatial.distance import cdist as distancematrix
from   scipy.spatial.distance import pdist as distancematrix
from   sklearn.cluster import DBSCAN

# Internal Dependencies
from .utility import ptrace, window, regen,  ParameterizedDefaultDict


"""Lamplight Module

This module houses interesting operations on images for lamplight analysis
"""

def image_info(filename):
    """
    Takes in a filename
    returns a tuple (filetype, basename(filename), numpy image)
    """
    img_type     = imghdr.what(filename)
    name, suffix = osp.basename(filename).rsplit('.', 1)
    src_image    = misc.imread(filename)
    return img_type, name, src_image


def empty_canvas(image):
    dst_image = np.array(image, copy=True)
    dst_img.fill(255)
    return dst_img


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
        print(save_modified(i, kwargs[i]))


@ptrace
def image_split(src_image):
    """
    split image to RBG and then saves them to dst directory

    # use by example with 'Extended Iterable Unpacking'
    r, g, b, *_ = image_split(src_image)
    """
    def np_one_color(keep_index__img):
        keep_index, img = keep_index__img
        """
        input image as an HxWxC numpy.array an index in range(C.len()) to preserve
        returns the image only preserving that color.
        """
        new = np.zeros(shape=img.shape)
        new[:,:,keep_index] = img[:,:,keep_index]
        return new

    np_lst = enumerate([src_image]*src_image.shape[2])
    return map(np_one_color, np_lst)


class step_range_gen(regen):
    """
    Object, probably needs documentation
    """
    def __init__(self, delta=10, maxvalue=255):
        gen = (maxvalue - i for i in range(0, maxvalue, delta))
        regen.__init__(self, gen)


@ptrace
def topograph_image(image, step_gen):
    """
    Takes in NxMxC numpy matrix and a step size and a delta
    returns  NxMxC numpy matrix with contours in each C cell
    """
    new_img = np.array(image, copy=True)

    """step_gen ~ (255, 245, 235, 225,...) """
    def myfunc(color):
        for tops, bots in window(step_gen, 2):
            if (color <= tops) and (color > bots):
                return tops
            if color > tops:
                break
        return 0

    topograph = np.vectorize(myfunc)
    return topograph(new_img)


@ptrace
def get_index_of(image, step_gen):
    """
    splits image into dict[band, intensity] as (x, y) point pairs
    this is used to shrink and split the search space for clustering

    this function is much more useful if run on result of topograph_image
    """
    ret = ParameterizedDefaultDict(GroupPoints)
    for x, col in enumerate(image):
        for y, pixel in enumerate(col):
            for band, intensity in enumerate(pixel):
                if intensity == next(step_gen):
                    ret[band, intensity].append(Coord(x,y))
    return ret


@ptrace
def make_clusters_dict(points_dict, step_gen, radius=20, minpoints=10):
    """
    Input:
      points_dict - dictionary of points indexed by d[band][intensity]
      step_gen    - valid band generator
      radius      - size of radius for ddbscan algorithm
      minpoints   - minimal number of points to be called a cluster
    Output:
      dict[band, intensity][cluster...] = [Coord(x, y)...]
    """
    @ptrace
    def make_clusters(d, band, intensity, radius, minpoints):
        """
        Takes in an iterable of (x, y) points
        returns a list of ClusterPoints
        """
        points    = d[band, intensity]
        xy_arrays = np.array(points)

        dbs = DBSCAN(radius, minpoints).fit(xy_arrays)

        core_samples = dbs.core_sample_indices_
        labels = dbs.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        clusters = [xy_arrays[labels == i] for i in range(n_clusters_)]

        retval = []

        def starmap(func, iterable):
            gunc = lambda x: func(*x)
            return map(gunc, iterable)

        for cluster in clusters:
            cp = ClusterPoints(band, intensity, starmap(Coord, cluster.tolist()))
            retval.append(cp)
        del d
        return retval

    retval = {}
    for band, intensity in points_dict:
        retval[band, intensity] = \
            make_clusters(points_dict, band, intensity, radius, minpoints)

    return retval


Coord = namedtuple('Coord', ['x', 'y'])

class GroupPoints(list):
    def __init__(self, band, intensity, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.__band      = band
        self.__intensity = intensity

    def append(self, value):
        if not isinstance(value, Coord):
            raise TypeError("value not Coord")
        list.append(self, value)

    def isband(self, band):
        return band == self.__band

    def isintensity(self, intenity):
        return intensity == self.__intensity


class ClusterPoints(GroupPoints):
    def __init__(self, band, intensity, *args, **kwargs):
        GroupPoints.__init__(self, band, intensity, *args, **kwargs)

    @property
    @ptrace
    def medoid(self):
        """
        given an iterable of (x, y) points, return the medoid
        """
        xy_arrays  = np.array(self, dtype=np.int16)
        matrix     = distancematrix(xy_arrays, metric='minkowski')
        key, value = min(enumerate(np.sum(matrix, axis=0)), key=itemgetter(1))

        return self[key]

    def overlaps(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("other does not share type")

        [small, large] = map(set, sorted([self, other], key=len))

        num = len(small.difference(large))
        den = len(small)

        return num/den


@ptrace
def simplexify(overlapped_clusters):
    """
    dict = {0: cr, 1: cg, 2: cb}
    """
    den = sum(map(len, overlapped_clusters.values()))
    ret = {}
    for key in overlapped_clusters:
        num      = len(overlapped_clusters[key])
        ret[key] = num/den

    ret['medoid'] = max(overlapped_clusters.values(), key=len).medoid

    return ret


@ptrace
def overlapping_clusters(cluster_dict, step_gen):
    """
    INPUT :
      dictionary[band, intensity][cluster...] = [(x, y)...]
    OUTPUT:
      yields overlapping clusters data as simplex dict + medoid
    """

    @ptrace
    def mostOverlapping(src, dsts, threshold=0.2):
        scores = map(src.overlaps, dsts)
        key, remaining = min(enumerate(scores), key = lambda e_v: e_v[1])
        return dsts[key] if remaining < threshold else []

    maxtensity   = next(step_gen)
    maxintensity = lambda b_i: b_i[1] == maxtensity

    d = {}
    for band, intensity in filter(maxintensity, cluster_dict):
        d[band] = cluster_dict[band, intensity] # re-index clusters

    it    = iter(d)
    fband = next(it) # select arbitrary band, may need to select largest
    rg    = regen(it)
    for cluster in d[fband]:
        p = {fband:cluster}
        for band in rg:
            p[band] = mostOverlapping(cluster, d[band])
        yield p


@ptrace
def colorize_clusters(base_img, color, *clusters):
    """
    clusters must be a dictionary

    Input base_img numpy array, and dictionary of clusters
    Outputs a copy of base_img with identified clusters filled with colors
    """
    new_img = np.array(base_img, copy=True)

    def colorize_my_cluster(c):
        for x, y in c:
            new_img[x, y][:3] = color

    for c in clusters:
        colorize_my_cluster(c)

    return new_img

