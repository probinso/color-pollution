#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""


from collections import OrderedDict
from contextlib  import contextmanager
from functools   import wraps

import glob
import hashlib
import itertools
import os.path as osp
import shutil
import sys
import tempfile
import time


global DEBUG
DEBUG = True

def simple_list(li):
    """
      takes in a list li
      returns a sorted list without doubles
    """
    return sorted(set(li))


def split_filter(li, cond, op=lambda x:x):
    """
      takes in list and conditional
      returns [[False], [True]] split list in O(n) time
    """
    retval = [[],[]]
    for elm in li:
        index = cond(elm)
        retval[index].append(op(elm) if index else elm)
    return retval


class regen(object):
    def __init__(self, generator):
        self.__generator = generator

    def __iter__(self):
        local, self.__generator = itertools.tee(self.__generator)
        return iter(local)

    def __next__(self):
        return next(iter(self))


def take(collection, num):
    """
    yields num elements from collection
    """
    for i, elm in enumerate(collection):
        if i >= num: break
        yield elm


def window(generator, size=2):
    """
    yields sliding window as list of specified size
    """
    it = iter(generator)
    win = [next(it) for _ in range(size)]
    yield win
    for rest in it:
        win.pop(0)
        win.append(rest)
        yield win


class ParameterizedDefaultDict(dict):
    def __init__(self, default, *args, **kwargs):
        assert(callable(default))
        self.__default = default
        super(self.__class__, self).__init__(self, *args, **kwargs)

    def __missing__(self, key):
        self[key] = self.__default(*key)
        return self[key]

    def __getitem__(self, *index):
        return super(self.__class__, self).__getitem__(*index)


class OrderedDefaultDict(OrderedDict):
    def __init__(self, default, *args, **kwargs):
        OrderedDict.__init__(self, *args, **kwargs)
        assert(callable(default))
        self.__default = default

    def __missing__(self, key):
        self[key] = self.__default()
        return self[key]


def ptrace(fn):
    def __get_time_hhmmss(diff):
        m, s = divmod(diff, 60)
        h, m = divmod(m, 60)
        time_str = "%02d:%02d:%02d" % (h, m, s)
        return time_str

    global DEBUG
    if DEBUG:
        @wraps(fn)
        def wrapped(*v, **k):
            name   = fn.__name__
            start  = time.time()
            retval =  fn(*v, **k)
            end    = time.time()
            time_str = __get_time_hhmmss(end - start)

            print(time_str, " :: ", name, file=sys.stderr)
            return retval
        return wrapped
    else:
        return fn


def path_walk(srcpath, suffix='*'):
    """
      Takes in dirpath and returns list of files and subdirectories
      (includes hidden)
    """
    # glob ignores hidden files.
    paths = glob.glob(osp.join(srcpath, suffix)) + \
            glob.glob(osp.join(srcpath, "." + suffix))

    [others, files] = split_filter(paths, osp.isfile)

    for directory in filter(osp.isdir, others):
        files += path_walk(directory)

    return files


def sign_path_list(*filenames):
    """
      input  :: list of filenames
      output :: unique identifier for set of filenames
    """

    def sign_path(filename, signature=None):
        """
          input  :: filename and accumulating signature
          output :: unique identifier for set of filename
        """
        with open(filename, mode='rb') as f:
            buf = osp.basename(filename)
            signature = sign_buffer(buf, signature)
            buf = f.read()
            signature = sign_buffer(buf, signature)

        return signature

    SIGTYPE = hashlib.sha1
    def sign_buffer(buf, signature=None):
        """
          input  :: buffer and accumulator signature
          output :: unique identifier for buffer
        """
        signature = SIGTYPE() if not signature else signature

        signature.update(SIGTYPE(buf).hexdigest())
        return signature

    signature = None
    for filename in simple_list(filenames):
        signature = sign_path(filename, signature)

    return signature


@contextmanager
def TemporaryDirectory(suffix='', prefix='tmp', dir=None, persist=False):
    """
      Like tempfile.NamedTemporaryFile, but creates a directory.
    """
    tree = tempfile.mkdtemp(suffix, prefix, dir)
    try:
        yield tree
    finally:
        if not persist:
            shutil.rmtree(tree)

