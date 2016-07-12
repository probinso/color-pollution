# -*- coding: utf-8 -*-"""
"""
This module administrates lamp clustering and feature extraction.
"""

import argparse, argcomplete
import sys

from .lamplight import image_info
from .lamplight import get_index_cond, make_clusters_dict, overlapping_clusters, simplify
from .topographical import check_topograph

from . import model as mod


def get_lamps(src_image, radius, size):
    points_dict  = get_index_cond(src_image)
    cluster_dict = make_clusters_dict(points_dict, radius, size)
    for i, raw_lamp in enumerate(overlapping_clusters(cluster_dict)):
        print("creating lamp : {}".format(i), file=sys.stderr)
        yield simplify(raw_lamp)


@mod.check_tables(mod.Cluster, 'lamps')
def check_cluster(topograph, radius, size):
    clst = make_cluster(radius, size, topograph)
    _, _, src_image = image_info(get_resource(topograph.dst_image.label))
    for simple_lamp in _get_lamps(src_image, radius, size):
        r, g, b = simple_lamp[0], simple_lamp[1], simple_lamp[2]
        x, y    = simple_lamp['medoid']
        min_x, min_y, max_x, max_y = simple_lamp['min_x'], simple_lamp['min_y'], simple_lamp['max_x'], simple_lamp['max_y']
        lamp    = make_lamp(clst, x, y, r, g, b, min_x, min_y, max_x, max_y)
    return {'radius' : radius, 'size' : size, 'topograph' : topograph}


@mod.db_session
def make_lamp(cluster, medoid_x, medoid_y, red, green, blue, min_x, min_y, max_x, max_y):
    cluster = mod.re_get(cluster)
    lamp = mod.Lamp(
        cluster=cluster,
        medoid_x=medoid_x, medoid_y=medoid_y,
        red=red, green=green, blue=blue,
        min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y
    )
    return lamp


def interface(filename, step, radius, size):
    resource = check_topograph(filename, step)
    for lamp in check_lamps(resource, step, radius, size):
        print(lamp)


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename  = arguments.image_filename
    radius    = arguments.radius
    size      = arguments.size
    step      = arguments.step
    interface(filename, step, radius, size)


#####################################
##         PARSERS
#####################################
def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image Filename to be clustered")
    parser.add_argument('--radius', type=int, default=30,
        help="Cluster acceptance radius")
    parser.add_argument('--size', type=int, default=20,
        help="Cluster minimum size")
    parser.add_argument('--step', type=int, default=10)
    parser.set_defaults(func=cli_interface)
    return parser
