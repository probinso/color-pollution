#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import os.path as osp
import sys

from .utility import location_resource, shutil

def interface():
    shutil.rmtree(location_resource('./'), True)


def cli_interface(arguments):
    interface()


def generate_parser(parser):
    parser.set_defaults(func=cli_interface)
    return parser
