#!/usr/bin/env python3
from   memory_profiler import profile

NUM    = 5

TOTS   = 100000000
lrange = lambda size : list(range(size))


def fun_flat():
    alist = lrange(TOTS)
    alen  = len(alist)
    print(alen)

    blist = lrange(TOTS)
    blen  = len(blist)
    print(blen)

    clist = lrange(TOTS)
    clen  = len(clist)
    print(clen)

    dlist = lrange(TOTS)
    dlen  = len(dlist)
    print(dlen)

    elist = lrange(TOTS)
    elen  = len(elist)
    print(elen)


def fun_nested():
    def nested():
        xlist = lrange(TOTS)
        xlen  = len(xlist)
        return xlen
    alen = nested()
    print(alen)

    blen = nested()
    print(blen)

    clen = nested()
    print(clen)

    dlen = nested()
    print(dlen)

    elen = nested()
    print(elen)


def fun_loop():
    pass





















from   timeit import timeit












"""
garbage_collector.collect()
print(timeit(fun_flat, number=1))

garbage_collector.collect()
print(timeit(fun_nested, number=1))

garbage_collector.collect()
print(timeit(fun_loop, number=1))



"""
