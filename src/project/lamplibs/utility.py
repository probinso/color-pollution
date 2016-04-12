#!/usr/bin/env python3
# -*- coding: utf-8 -*-"""


from collections import OrderedDict, Iterable
from contextlib  import contextmanager
from functools   import wraps, partial

import glob
import hashlib
import itertools
import os
import os.path as osp
import shutil
import sys
import tempfile
import time
import xdg.BaseDirectory



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


def test_path(path):
    if not osp.exists(path):
        raise FileNotFoundError("File error: {} does not exist".format(path))
    return path


def location_resource(
  fname='.',
  location=xdg.BaseDirectory.save_data_path('lamplibs')
  ):
    return osp.join(location, fname)


def get_resource(fname='.'):
    path = location_resource(fname=fname)
    return test_path(path)


def commit_resource(full_path):
    srcdir, fname = osp.split(test_path(full_path))
    label = sign_path(full_path)
    copy_directory_files(srcdir, location_resource(), [fname])
    src = partial(osp.join, location_resource())
    os.rename(src(fname), src(label))
    return label


def copy_directory_files(srcdir, dstdir, filenames):
    """
      copies [filenames] from srcdir to dstdir
    """
    for filename in filenames:
        srcpath = osp.join(srcdir, filename)
        dstpath = osp.join(dstdir, filename)
        shutil.copyfile(srcpath, dstpath)


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
        if not isinstance(key, Iterable):
            key = key,

        self[key] = self.__default(*key)
        return self[key]

    def __getitem__(self, *index):
        return super(self.__class__, self).__getitem__(*index)

    def __call__(self, *args):
        # so that self.__class__ can be used as a memoizer
        return self[args]


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


def sign_path(filename, SIGTYPE=hashlib.md5):
    """
    input  :: filename and accumulating signature
    output :: unique identifier for set of filename
    """
    with open(filename, mode='rb') as f:
        d = SIGTYPE()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)

    return d.hexdigest()


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

