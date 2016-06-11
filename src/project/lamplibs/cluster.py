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

"""
def select_clusters(image, radius, size):

    def paint(src_img, dst_img):
        points_dict  = get_index_cond(src_img)
        cluster_dict = make_clusters_dict(points_dict, radius, size)

        order = lambda o: len(o[1])
        for i, overlapping in enumerate(overlapping_clusters(cluster_dict)):
            print("visiting lamp : {}".format(i))
            print(simplexify(overlapping), file=sys.stdout)
            for key, clstr in sorted(overlapping.items(), key=order, reverse=True):
                col      = [0, 0, 0]
                col[key] = 255
                dst_img = colorize_clusters(dst_img, col, clstr)

        return dst_img

    dst_img  = empty_canvas(image)
    save_img = paint(image, dst_img)

    return save_img
"""


@mod.pny.db_session
def check_lamps(resource, step, radius, size):
    top  = mod.Topograph.get(dst_image=resource, step=step)
    clst = mod.Cluster.get(topograph=top, radius=radius, size=size)
    if not clst:
        clst  = mod.Cluster(topograph=top, radius=radius, size=size)
        _, _, src_image = image_info(mod.get_resource(resource))
        local_lamps = []
        for simple_lamp in get_lamps(src_image, radius, size):
            local_lamps.append(
                mod.Lamp(cluster=clst,
                         red=simple_lamp[0],
                         green=simple_lamp[1],
                         blue=simple_lamp[2],
                         medoid_x=simple_lamp['medoid'].x,
                         medoid_y=simple_lamp['medoid'].y)
            )
    return map(lambda obj: getattr(obj, 'feature_vector'), clst.lamps)


def get_lamps(src_image, radius, size):
    points_dict  = get_index_cond(src_image)
    cluster_dict = make_clusters_dict(points_dict, radius, size)
    for i, raw_lamp in enumerate(overlapping_clusters(cluster_dict)):
        print("creating lamp : {}".format(i), file=sys.stderr)
        yield simplify(raw_lamp)


def interface(filename, step, radius, size):
    resource = check_topograph(filename, step)
    #img_type, name, src_image = image_info(mod.get_resource(resource))
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
