#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

# EXTERNAL PACKAGES
import argparse, argcomplete
import sys

# INTERNAL PACKAGES
from . import cluster
from . import extractRGB as rgb
from . import topographical


def cluster_parser(subparsers):
    parser = subparsers.add_parser('cluster')
    cluster.generate_parser(parser)
    return parser


def extractRGB_parser(subparsers):
    parser = subparsers.add_parser('rgb')
    rgb.generate_parser(parser)
    return parser


def topograph_parser(subparsers):
    parser = subparsers.add_parser('topograph')
    topographical.generate_parser(parser)
    return parser


def generate_parser(parser):
    subparsers = parser.add_subparsers(help="subcommand")

    cluster_parser(subparsers)
    extractRGB_parser(subparsers)
    topograph_parser(subparsers)
    return parser


def main():
    parser = argparse.ArgumentParser(description='Color Pollution Course Libs')
    generate_parser(parser)
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()

    if hasattr(arguments, 'func'):
        sys.exit(arguments.func(arguments))


if __name__ == "__main__":
    main()