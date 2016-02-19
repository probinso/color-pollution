#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

from collections import Counter
import functools, itertools
import time

global DEBUG
DEBUG = True

global fc
fc = Counter()


def take(collection, num):
    """
    yields num elements from collection
    """
    for i, elm in enumerate(collection):
        if i >= num: break
        yield elm


def ptrace(fn):
    def __get_time_hhmmss(diff):
        m, s = divmod(diff, 60)
        h, m = divmod(m, 60)
        time_str = "%02d:%02d:%02d" % (h, m, s)
        return time_str

    global DEBUG, fc
    if DEBUG:
        def wrapped(*v, **k):
            name     = fn.__name__
            fc.update([name])

            start  = time.time()
            retval =  fn(*v, **k)
            end    = time.time()
            time_str = __get_time_hhmmss(end - start)

            print time_str, " :: ", name
            return retval
        return wrapped
    else:
        return fn

