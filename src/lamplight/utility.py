#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

from collections import Counter, OrderedDict
import functools, itertools
import time

global DEBUG
DEBUG = True

global fc
fc = Counter()

class regen(object):
    def __init__(self, generator):
        self.__generator = generator

    def __iter__(self):
        local, self.__generator = itertools.tee(self.__generator)
        for elm in local:
            yield elm


def take(collection, num):
    """
    yields num elements from collection
    """
    for i, elm in enumerate(collection):
        if i >= num: break
        yield elm


def window(generator, size=2):
    it = iter(generator)
    win = [next(it) for _ in range(size)]
    yield win
    for rest in it:
        win = win[1:] + [rest]
        yield win


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

    global DEBUG, fc
    if DEBUG:
        def wrapped(*v, **k):
            name     = fn.__name__
            fc.update([name])

            start  = time.time()
            retval =  fn(*v, **k)
            end    = time.time()
            time_str = __get_time_hhmmss(end - start)

            print(time_str, " :: ", name)
            return retval
        return wrapped
    else:
        return fn


class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

