#!/usr/bin/env python

import gc as garbage_collector
from   memory_profiler import profile

from   timeit import timeit

TOTS = 100000000


@profile
def fun_hog():
    alist = range(TOTS)
    alen  = len(alist)
    print alen

    blist = range(TOTS)
    blen  = len(blist)
    print blen

    xlist = range(TOTS)
    xlen  = len(xlist)
    print xlen

    ylist = range(TOTS)
    ylen  = len(ylist)
    print ylen

    zlist = range(TOTS)
    zlen  = len(zlist)
    print zlen


@profile
def fun_nested():
    def helper():
        hlist = range(TOTS)
        hlen  = len(hlist)
        return hlen

    alen = helper()
    print alen

    blen = helper()
    print blen

    xlen = helper()
    print xlen    

    ylen = helper()
    print ylen    

    zlen = helper()
    print zlen


@profile
def fun_loop():
    for _ in xrange(5):
        hlist = range(TOTS)
        hlen  = len(hlist)
        print hlen


garbage_collector.collect()
print timeit(fun_hog, number=1)

garbage_collector.collect()
print timeit(fun_nested, number=1)

garbage_collector.collect()
print timeit(fun_loop, number=1)
