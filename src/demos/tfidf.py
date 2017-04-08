#!/usr/bin/env python

import csv
from sortedcontainers import SortedDict, SortedList
from collections import namedtuple

class SortedDefaultDict(SortedDict):
    def __init__(self, constructor, *args, **kwargs):
        SortedDict.__init__(self, *args, **kwargs)
        assert(callable(constructor))
        self.__constructor = constructor

    def __missing__(self, key):
        self[key] = self.__constructor()
        return self[key]

lookup = SortedDefaultDict(SortedList)
TF = namedtuple("TF", ["id", "count"])

with open("./docs.csv") as fd:
    for doc_id, contents in csv.reader(fd):
        tokens = contents.split()
        for word in set(tokens):
            lookup[word].add(TF(doc_id, tokens.count(word)))

for word in lookup:
    print(word, ":")
    for doc in lookup[word]:
        print("   ", doc.id, doc.count/len(lookup[word]))

