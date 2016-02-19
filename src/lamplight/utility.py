#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

import functools, itertools

global DEBUG
DEBUG = True


def take(collection, num):
    """
    yields num elements from collection
    """
    for i, elm in enumerate(collection):
        if i >= num:
            break
        yield elm


def ptrace(fn):
    global DEBUG
    if DEBUG:
        def wrapped(*v, **k):
            name = fn.__name__
            print name
            return fn(*v, **k)
        return wrapped
    else:
        return fn

