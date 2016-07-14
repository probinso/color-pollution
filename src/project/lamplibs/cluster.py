# -*- coding: utf-8 -*-"""
"""
This module administrates lamp clustering and feature extraction.
"""

import argparse, argcomplete
import sys

from .lamplight import image_info
from .lamplight import get_index_cond, make_clusters_dict, overlapping_clusters, simplify
from .topographical import check_topograph
from .register import commit_register_image_file
from .utility import get_resource

from . import model as mod


def _get_lamps(src_image, radius, size):
    points_dict  = get_index_cond(src_image)
    cluster_dict = make_clusters_dict(points_dict, radius, size)
    for raw_lamp in overlapping_clusters(cluster_dict):
        yield simplify(raw_lamp)


@mod.db_session
def make_cluster(radius, size, topograph):
    topograph = mod.re_get(topograph)
    clst = mod.Cluster.get(radius=radius, size=size, topograph=topograph)
    if not clst:
        clst = mod.Cluster(radius=radius, size=size, topograph=topograph)
    return clst


@mod.check_tables(mod.Cluster, feature='lamps', debug=True)
def check_cluster(topograph, radius, size):
    clst = make_cluster(radius, size, topograph)
    _, _, src_image = image_info(get_resource(topograph.dst_image.label))
    for simple_lamp in _get_lamps(src_image, radius, size):
        lamp = make_lamp(cluster=clst, **simple_lamp)
    return {'radius' : radius, 'size' : size, 'topograph' : topograph}


@mod.db_session
def make_lamp(**kwargs):
    kwargs['cluster'] = mod.re_get(kwargs['cluster'])
    lamp = mod.Lamp(**kwargs)
    return lamp


def interface(filename, step, radius, size):
    src_image = commit_register_image_file(filename)
    topograph = check_topograph(src_image, step)
    for lamp in check_cluster(topograph, radius, size):
        print(lamp.feature_vector)


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename = arguments.image_filename
    radius   = arguments.radius
    size     = arguments.size
    step     = arguments.step
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
