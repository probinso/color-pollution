#!/usr/bin/env python


def mutable_base_collections():
    def list_behaviour():
        # a list stores elements
        l = []       # []
        l.append(5)  # [5]
        l.append(4)  # [5, 4]
        l.append(5)  # [5, 4, 5]
        l.append(7)  # [5, 4, 5, 7]
        for element in l:
            print element

        print l[0]   # 5
        print l[-1]  # 7

    def set_behaviour():
        # a set stores elements without order or repetition
        s = set() # set([])
        s.add(5)  # set([5])
        s.add(4)  # set([4, 5])
        s.add(5)  # set([4, 5])
        s.add(7)  # set([4, 5, 7])
        for element in s:
            print element

    def dictionary_behaviour():
        # dictionary stores unordered key->value pairs
        d = {}          # {}
        d['first' ] = 5 # {'first' : 5}
        d['second'] = 4 # {'second': 4, 'first': 5}
        d['third' ] = 5 # {'second': 4, 'third': 5, 'first': 5}
        d['fourth'] = 7 # {'second': 4, 'third': 5, 'first': 5, 'fourth': 7}
        for key in d:
            print key, d[key]

    list_behaviour()
    set_behaviour()
    dictionary_behaviour()

mutable_base_collections()


from collections import OrderedDict
def example():
    # dictionary stores ordered key->value pairs
    o = OrderedDict()
    o['first' ] = 5 # {'first': 5}
    o['second'] = 4 # {'first': 5, 'second': 4}
    o['third' ] = 5 # {'first': 5, 'second': 4, 'third': 5}
    o['fourth'] = 7 # {'first': 5, 'second': 4, 'third': 5, 'fourth': 7}
    for key in o:
        print key, o[key]

example()


from collections import defaultdict
def example():
    # dictionary that you don't have to initinalize
    dd = defaultdict(list)
    for word in ['first', 'second', 'third', 'fourth']:
        char = word[0]
        dd[char].append(word)

    # {'s': ['second'], 't': ['third'], 'f': ['first', 'fourth']}
    for key in dd:
        for word in dd[key]:
            print word

example()


class OrderedDefaultDict(OrderedDict):
    def __init__(self, default, *args, **kwargs):
        assert(callable(default))
        self.__default = default
        OrderedDict.__init__(self, *args, **kwargs)

    def __missing__(self, key):
        self[key] = self.__default()
        return self[key]

def example():
    # dictionary that you don't have to initalize and preserves order
    dod = OrderedDefaultDict(list)
    for word in ['first', 'second', 'third', 'fourth']:
        char = word[0]
        dod[char].append(word)

    # {'f': ['first', 'fourth'], 's': ['second'], 't': ['third']}
    for key in dod:
        for word in dod[key]:
            print word

example()


from collections import namedtuple
def example():
    Point  = namedtuple('Point', ['x', 'y'])

    points = [Point(5, 5), Point(4, 9)]
    for x, y in points:
        print x, y

    for p in points:
        x, y = p
        print x, y

    for p in points:
        print p.x, p.y

    for p in points:
        print p[0], p[1]

example()
