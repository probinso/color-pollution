
import argparse, argcomplete
import sys
import os.path as osp

from shutil import move

from .cluster   import check_lamps, check_topograph
from .utility   import TemporaryDirectory
from .lamplight import pie_canvas, image_info
from .          import model as mod


def interface(filename, dst, step, radius, size):
    resource = check_topograph(filename, step)
    _img_type, _name, src_image = image_info(mod.get_resource(resource))

    with TemporaryDirectory(persist=True) as dd:
        src_image = commit_register_image_file(filename)
        topograph = check_topograph(src_image, step)
        lamps = (lamp for lamp in check_cluster(topograph, radius, size)

        fname = pie_canvas(dd, src_image.shape, *lamps)
        move(fname, osp.join(dst, 'output.png'))


def cli_interface(arguments):
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    filename  = arguments.image_filename
    radius    = arguments.radius
    size      = arguments.size
    step      = arguments.step
    dst       = arguments.dst_directory
    interface(filename, dst, step, radius, size)


#####################################
##         PARSERS
#####################################
def generate_parser(parser):
    parser.add_argument('image_filename', type=str,
        help="Image Filename to be clustered")
    parser.add_argument('dst_directory', type=str,
        help="Location to save modified images")
    parser.add_argument('--radius', type=int, default=30,
        help="Cluster acceptance radius")
    parser.add_argument('--size', type=int, default=20,
        help="Cluster minimum size")
    parser.add_argument('--step', type=int, default=10)
    parser.set_defaults(func=cli_interface)
    return parser
