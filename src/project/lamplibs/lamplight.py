# -*- coding: utf-8 -*-"""
"""
This module encapsulates the logic of the model view controller.

Classes Provided:
  GroupPoints(list)
    a list of ('Coord', ['x', 'y']).

  ClusterPoints(GroupPoints)
    extends GroupPoints with 'medoid(self)' and 'overlaps(self, other)' methods.
"""

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
from   scipy.spatial.distance import cdist as distancematrix
from   sklearn.cluster import DBSCAN

# Internal Dependencies
from .utility import window, regen, ParameterizedDefaultDict


"""Lamplight Module

This module houses interesting operations on images for lamplight analysis
"""

def image_info(filename):
    """
    Takes in a filename
    returns a tuple (filetype, basename(filename), numpy image)
    """
    img_type    = imghdr.what(filename)
    name, *_ext = osp.basename(filename).rsplit('.', 1)
    src_image   = misc.imread(filename)
    return img_type, name, src_image


def empty_canvas(image):
    dst_img = np.array(image, copy=True)
    dst_img.fill(255)
    return dst_img


def save_images(dst, name, img_type='png', **kwargs):
    """
    input:
      dst  is a directory destination
      name is the expected name of the image to be saved
      img_type is the saving filetype
      kwargs is dictionary of numpy image arrays
    output:
      saves images into dst with name in bmp format
    """

    def save_modified(prefix, image):
        result = osp.join(dst, prefix + name + '.' + img_type)
        misc.imsave(result, image)
        return result

    li = [save_modified(i, kwargs[i]) for i in kwargs]
    return li


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


class _step_range_gen(regen):
    """
    Object, probably needs documentation
    """
    def __init__(self, delta=10, maxvalue=255):
        gen = (maxvalue - i for i in range(0, maxvalue, delta))
        regen.__init__(self, gen)


def topograph_image(image, step):
    """
    Takes in NxMxC numpy matrix and a step size and a delta
    returns  NxMxC numpy matrix with contours in each C cell
    """
    step_gen = _step_range_gen(step)
    new_img  = np.array(image, copy=True)

    """step_gen ~ (255, 245, 235, 225,...) """
    def myfunc(color):
        for tops, bots in window(step_gen, 2):
            if (color <= tops) and (color > bots):
                return tops
            if color > tops:
                break
        return 0

    topograph = np.vectorize(myfunc)
    return new_img if step == 1 else topograph(new_img)


def get_index_cond(image, cond=lambda x: x == 255):
    """
    splits image into dict[band, intensity] as (x, y) point pairs
    this is used to shrink and split the search space for clustering

    this function is much more useful if run on result of topograph_image
    additionally, This function works very poorly on lossy image formats
    """
    ret = ParameterizedDefaultDict(GroupPoints)
    for x, col in enumerate(image):
        for y, pixel in enumerate(col):
            for band, intensity in enumerate(pixel):
                if band == 3: continue # transparentcy is not applicable
                if cond(intensity):
                    ret[band, intensity].append(Coord(x,y))
    return ret


def make_clusters_dict(points_dict, radius=20, minpoints=10):
    """
    Input:
      points_dict - dictionary of points indexed by d[band][intensity]
      radius      - size of radius for ddbscan algorithm
      minpoints   - minimal number of points to be called a cluster
    Output:
      dict[band, intensity][cluster...] = [Coord(x, y)...]
    """
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
    def medoid(self):
        """
        given an iterable of (x, y) points, return the medoid
        """
        xy_arrays = np.array(self)
        matrix    = distancematrix(xy_arrays, xy_arrays, metric='sqeuclidean')
        key, _    = min(enumerate(map(np.sum, matrix)), key=itemgetter(1))

        return self[key]

    def overlaps(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("other does not share type")

        [small, large] = map(set, sorted([self, other], key=len))

        num = len(small.difference(large))
        den = len(small)

        return num/den


def simplify(overlapped_clusters):
    """
    dict = {0: cr, 1: cg, 2: cb}
    """
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    den = sum(map(len, overlapped_clusters.values()))
    ret = {}
    for key in overlapped_clusters:
        num      = len(overlapped_clusters[key])
        for x, y in overlapped_clusters[key]:
            min_x = x if x < min_x else min_x
            min_y = y if y < min_y else min_y
            max_x = x if x > min_x else min_x
            max_y = y if y > min_y else min_y
        ret[key] = num

    # medoids only exist on non-empty lists of points
    ret['medoid'] = min(filter(bool, overlapped_clusters.values()), key=len).medoid
    ret['min_x']  = min_x
    ret['min_y']  = min_y
    ret['max_x']  = max_x
    ret['max_y']  = max_y
    return ret


def overlapping_clusters(cluster_dict):
    """
    INPUT :
      dictionary[band, intensity][cluster...] = [(x, y)...]
    OUTPUT:
      yields overlapping clusters data as simplex dict + medoid
    """
    def mostOverlapping(src, dsts, threshold=0.2):
        """
        returns the largest cluster who is most overlapping with src in [dsts...]

        note that 'sorted' is a stable sorting algorithm
        """
        scores = map(src.overlaps, sorted(dsts, key=len, reverse=True))
        key, remaining = min(enumerate(scores), key=itemgetter(1))
        return dsts[key] if remaining < threshold else []

    d = {}
    for band, intensity in cluster_dict:
        d[band] = cluster_dict[band, intensity] # re-index clusters

    fband, *rg = iter(d)
    for cluster in d[fband]:
        p = {fband:cluster}
        for band in rg:
            p[band] = mostOverlapping(cluster, d[band])
        yield p


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

import matplotlib.pyplot as plt
from math import sqrt, ceil

def pie(tumpdir, *lamps):
    colors = ['red', 'green', 'blue']
    for lamp in lamps:
        sizes = [lamp[x] for x in colors]
        patches, _ = plt.pie(sizes, colors=colors, startangle=90)
        plt.axis('equal')
        plt.tight_layout()
        itemgetter(list(), 0)
        filename = osp.join(tumpdir, 'foo.png')
        plt.savefig(filename, bbox_inches='tight', transparent=True)
        plt.close()
        size = lamp['radius']
        yield filename, size, lamp['medoid_x'], lamp['medoid_y']


from PIL import Image, ImageChops

@ptrace
def pie_canvas(tumpdir, shape, *lamps):

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return im.crop(bbox) if bbox else im

    bg_h, bg_w, *_  = shape
    background = Image.new('RGBA', (bg_w, bg_h), (255, 255, 255, 255))

    for filename, file_size, loc_y, loc_x in pie(tumpdir, *lamps):
        print(file_size, loc_x, loc_y)
        img = Image.open(filename, 'r')
        img = trim(img)

        img.thumbnail((file_size, file_size), Image.ANTIALIAS)
        img_w, img_h = file_size, file_size
        offset =  loc_x - file_size // 4, loc_y - file_size // 4
        background.paste(img, offset, mask=img)
        img.close()
        #filename, file_size, loc_y, loc_x = 0, 0, 0, 0

    dst = osp.join(tumpdir, 'out.png')
    background.save(dst)
    return dst
