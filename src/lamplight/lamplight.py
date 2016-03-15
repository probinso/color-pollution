#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""

from   collections import namedtuple

# from   itertools   import imap
imap   = map
xrange = range

from   math        import sqrt
from   operator    import itemgetter
import os.path as osp

import ddbscan
import imghdr
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc as misc

from   utility import take, ptrace, window
from   utility import OrderedDefaultDict as defaultdict

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
    import pylab as plt
    @ptrace
    def save_modified(prefix, image):
        result = osp.join(dst, prefix + name + "." + img_type)
        misc.imsave(result, image)
        plt.imshow(image)
        return result

    for i in kwargs:
        save_modified(i, kwargs[i])


def image_split(src_image, channels=3):
    """
    split image to RBG and then saves them to dst directory
    uses process pool to speed up function

    we can get rid of channels by using 'Extended Iterable Unpacking'
    however this is not yet in the language
    """
    def np_one_color(keep_index__img):
        keep_index, img = keep_index__img # python3 compliance
        """
        input image as an HxWxC numpy.array an index in range(C.len()) to preserve
        returns the image only preserving that color.
        """
        new = np.zeros(shape=img.shape)
        new[:,:,keep_index] = img[:,:,keep_index]
        return new

    np_lst = enumerate([src_image]*src_image.shape[2])
    return map(np_one_color, np_lst)[:channels]


from utility import regen
class step_range_gen(regen):
    """
    Object, probably needs documentation
    """
    xrange = range
    def __init__(self, delta=10, maxvalue=255):
        gen = (maxvalue - i for i in xrange(0, maxvalue, delta))
        regen.__init__(self, gen)


@ptrace
def topograph_image(image, step_gen):
    """
    Takes in NxMxC matrix and a step size and a delta
    returns NxMxC matrix with contours in each C cell
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
def get_index_of(image):
    """
    splits image into dict[channel][intensity] as (x, y) point pairs
    this is used to shrink and split the search space for clustering

    this function is much more useful if run on result of topograph_image
    """
    ret = defaultdict(lambda : defaultdict(cluster))
    for x, column in enumerate(image):
        for y, pixel in enumerate(column):
            for channel, intensity in enumerate(pixel):
                ret[channel][intensity].append(Coord(x,y))
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
      dictionary[intensity][cluster_id][band] = [(x, y)]
    """
    @ptrace
    def make_clusters(points, radius, minpoints):
        """
        Takes in an iterable of (x, y) points
        returns a dict of lists of points
        """
        scan = ddbscan.DDBSCAN(radius, minpoints)
        for p in points:
            scan.add_point(p, count=1, desc="")

        scan.compute()

        """
        for index, cluster in enumerate(scan.clusters):
            print('=== Cluster %d ===' % index)
            print('Cluster points index: %s' % len(list(cluster)))
        """

        d = defaultdict(cluster)
        for i, p in enumerate(scan.points):
            if scan.points_data[i].cluster == -1:
                # cluster_id == -1 is an anomolous point
                continue
            d[scan.points_data[i].cluster].append(Coord(*p))

        return d

    retval = defaultdict(lambda : defaultdict(cluster))
    for l_intensity in take(step_gen, 3):
        for l_channel in points_dict:
            retval[l_channel][l_intensity] = \
              make_clusters(points_dict[l_channel][l_intensity], radius, minpoints)

    return retval


Coord = namedtuple('Coord', ['x', 'y'])

class cluster(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    @property
    def medoid(self):
        """
        given an iterable of (x, y) points, return the medoid
        """
        def average_dissimilarity(loc):
            def dist(x_y, p_q):
                x, y = x_y
                p, q = p_q
                return sqrt((x-p)**2 + (y-p)**2)
            # python3 compliance
            # dist = lambda (x, y), (p, q): sqrt((x-p)**2 + (y-q)**2)

            def f(points):
                tots = sum((dist(loc, p) for p in points))
                return tots / len(points)

            return f

        averages = (fun(self) for fun in imap(average_dissimilarity, self))
        key = min(enumerate(averages), key=itemgetter(1))[0]

        return self[key]

    def overlaps(self, other, threshold=0.05):
        if not isinstance(other, type(self)):
            raise TypeError("other does not share type")

        [small, large] = map(set, sorted([self, other], key=len))

        num = len(small.difference(large))
        den = len(small)

        return ((num/float(den)) < threshold)

    def append(self, value):
        if not isinstance(value, Coord):
            raise TypeError("value not Coord")
        list.append(self, value)


@ptrace
def overlapping_clusters(cluster_dict, step_gen):
    """
    INPUT :
      dictionary[band][intensity][cluster_id] = [(x, y)...]

      because cluster_id is effectively arbitrary, this
      information isn't preserved
    OUTPUT:
      dictionary[intensity][cluster][band] = [(x, y)...]
    """

    bit       = iter(cluster_dict)
    band      = next(bit)
    intensity = next(step_gen)

    cid = next(iter(cluster_dict[band][intensity]))

    retval = defaultdict(lambda: defaultdict(lambda: defaultdict(cluster)))
    for intensity in take(step_gen, 3):
        it     = iter(cluster_dict)
        f_band = next(it)

        for f_cluster_id, f_cluster in cluster_dict[f_band][intensity].items():

            retval[intensity][f_cluster_id][f_band] = f_cluster
            for i_band in it:
                MATCH_IN_BAND = False
                for i_cluster in cluster_dict[i_band][intensity].values():
                    if f_cluster.overlaps(i_cluster):
                        retval[intensity][f_cluster_id][i_band] = i_cluster
                        MATCH_IN_BAND = True
                        break
                # only one match per band/intensity/cluster tuple
                if MATCH_IN_BAND: break

    return retval


@ptrace
def paint_points(base_img, points, color=[0, 0, 0], channels=3):
    """
    Takes in base_img, iterable of points (x, y), color, and default channels
    """
    new_img = np.array(base_img, copy=True)
    for x, y in points:
        new_img[x, y] = color[:channels]
    return new_img


@ptrace
def colorize_clusters(base_img, clusters):
    """
    clusters must be a dictionary

    Input base_img numpy array, and dictionary of clusters
    Outputs a copy of base_img with identified clusters filled with colors
    """
    new_img = np.array(base_img, copy=True)
    colors  = plt.cm.Spectral(np.linspace(0 , 1, len(clusters)))*255

    @ptrace
    def colorize_my_cluster(i, c):
        for x, y in clusters[c]:
            new_img[x, y] = colors[i][:3]

    #mykey = lambda (i, (a, b)): len(b)
    def mykey(i__a_b):# python3 compliance, which i find dumb
        (i, (a, b)) = i__a_b
        return b

    for i, (c, _) in sorted(enumerate(clusters.viewitems()), key=mykey, reverse=True):
        print("welcome to channel", i)
        colorize_my_cluster(i, c)

    return new_img

