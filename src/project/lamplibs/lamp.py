#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-"""
"""
This module administrates the CLI of each existing subcommand.
"""

# EXTERNAL PACKAGES
import argparse, argcomplete
import sys

# INTERNAL PACKAGES
from . import purge
from . import cluster
from . import extractRGB as rgb
from . import topographical
from . import register

def cluster_parser(subparsers):
    parser = subparsers.add_parser('cluster')
    cluster.generate_parser(parser)
    return parser


def extractRGB_parser(subparsers):
    parser = subparsers.add_parser('rgb')
    rgb.generate_parser(parser)
    return parser


def register_parser(subparsers):
    parser = subparsers.add_parser('register')
    register.generate_parser(parser)
    return parser


def purge_parser(subparsers):
    parser = subparsers.add_parser('purge')
    purge.generate_parser(parser)
    return parser


def topograph_parser(subparsers):
    parser = subparsers.add_parser('topograph')
    topographical.generate_parser(parser)
    return parser


def generate_parser(parser):
    subparsers = parser.add_subparsers(help="subcommand")

    cluster_parser(subparsers)
    extractRGB_parser(subparsers)
    register_parser(subparsers)
    purge_parser(subparsers)
    topograph_parser(subparsers)
    return parser


def main():
    parser = argparse.ArgumentParser(
        description='Color Pollution Course Libs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser = generate_parser(parser)
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()

    if hasattr(arguments, 'func'):
        ret = arguments.func(arguments)
    else:
        ret = parser.print_help()
    sys.exit(ret)

if __name__ == "__main__":
    main()
