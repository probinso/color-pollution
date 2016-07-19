#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-"""
"""
This module provides operational support for purging the Model's database.
"""

import argparse, argcomplete
import os.path as osp
import sys

from . import model as mod
from .utility import location_resource, shutil

def interface(force):
    def yes_or_no(question):
        reply = str(input(question+' (y/n): ')).lower().strip()
        return reply[0] == 'y' if reply else False

    if not force:
        force = yes_or_no("are you sure you want to purge?")

    if force:
        shutil.rmtree(location_resource('./'), True)
        mod.db.drop_all_tables(with_all_data=True)
        print("store purged")
    else:
        print("purge ignored")


def cli_interface(arguments):
    force = arguments.force
    interface(force)


def generate_parser(parser):
    parser.add_argument('-f', dest='force', action='store_true', default=False,
        help="skip prompt")
    parser.set_defaults(func=cli_interface)
    return parser
