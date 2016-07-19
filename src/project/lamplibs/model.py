# -*- coding: utf-8 -*-"""
"""
This module describes the Model in our Model View Controller.
"""

import inspect
import json

import os.path  as osp
import pony.orm as pny

from  shutil    import copy
from .utility   import ptrace, sign_path
from .lamplight import image_info

'https://editor.ponyorm.com/user/probinson/lamplibs'

from . import utility

VERSION = sign_path(inspect.getfile(inspect.currentframe()))

db = pny.Database()


with open('secrets.json') as cred_file: credentials = json.load(cred_file)
db.bind('postgres', **credentials['db'])

import boto3
client = boto3.client('s3', **credentials['s3'])

def get_resource(fname):
    _ = utility.location_resource(fname)
    bucket = client.download_file('pollution.alpha', fname, _)
    return _


def commit_resource(full_path):
    label = utility.commit_resource(full_path)
    client.upload_file(full_path, 'pollution.alpha', label)
    return label


from functools import wraps, partial


def db_session(func):
    @wraps(func)
    @pny.db_session(retry=5)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def re_get(orm_obj):
    def todict(x):
        d = dict()
        for col in x._columns_:
            try:
                tump = getattr(x, col)
            except: # sloppy
                continue
            if isinstance(tump, pny.core.SetInstance):
                continue

            if isinstance(tump, pny.core.Entity):
                tump = re_get(tump)
            d[col] = tump
        return d
    return orm_obj.__class__.get(**todict(orm_obj))


def check_tables(cls, feature=None):
    f_args = lambda f: [x for x in inspect.getargspec(f)[0]]

    def re_orm(kwargs):
        for key in kwargs:
            if isinstance(kwargs[key], pny.core.Entity):
                kwargs[key] = re_get(kwargs[key])
        return kwargs

    def real_decorator(work):
        assert(all(x in cls._columns_ for x in f_args(work)))

        def useful_return(entry):
            if entry:
                ret = getattr(entry, feature) if feature else entry
                return {x for x in ret} if isinstance(ret, pny.core.SetInstance) else ret
            return entry

        @db_session
        def get_entry(**kwargs):
            kwargs = re_orm(kwargs)
            entry  = cls.get(**kwargs)
            return useful_return(entry)

        @db_session
        def add_entry(**kwargs):
            kwargs = re_orm(kwargs)
            entry  = cls.get(**kwargs)
            if not entry:
                entry = cls(**kwargs)
            return useful_return(entry)

        @wraps(work)
        def wrapper(*args):
            kwargs = dict(zip(f_args(work), args))
            contents = get_entry(**kwargs)
            if not contents:
                key_dict = ptrace(work)(*args)
                contents = add_entry(**key_dict)
            return contents

        return wrapper

    return real_decorator


class Image(db.Entity):
    _table_  = "tbl_image"
    label    = pny.PrimaryKey(str)
    img_type = pny.Required(str)
    height   = pny.Required(int)
    width    = pny.Required(int)

    topograph  = pny.Optional("Topograph", reverse="dst_image")
    top_images = pny.Set("Topograph", reverse="src_image")

    @property
    def data(self):
        *_, data = image_info(get_resource(self.label))
        return data


@db_session
def retrieve_image(resource, destination, rename='output'):
    img = Image.get(label=resource)
    if not img:
        raise FileNotFoundError("database resource '{}'".format(resource))
    savename = rename + '.' + img.img_type
    copy(get_resource(resource), osp.join(destination, savename))


class Topograph(db.Entity):
    _table_   = "tbl_topograph"
    dst_image = pny.PrimaryKey(Image, reverse="topograph")
    step      = pny.Required(int)
    src_image = pny.Required(Image, reverse="top_images")
    cluster_images = pny.Set("Cluster")


class Cluster(db.Entity):
    _table_   = "tbl_cluster"
    radius    = pny.Required(int)
    size      = pny.Required(int)
    lamps     = pny.Set("Lamp")
    topograph = pny.Required(Topograph)


class Lamp(db.Entity):
    _table_  = "tbl_lamp"

    cluster  = pny.Required(Cluster)
    red      = pny.Optional(int)
    green    = pny.Optional(int)
    blue     = pny.Optional(int)

    medoid_x = pny.Required(int)
    medoid_y = pny.Required(int)
    min_x, min_y = pny.Required(int), pny.Required(int)
    max_x, max_y = pny.Required(int), pny.Required(int)

    @property
    def feature_vector(self):
        _   = ['red', 'green', 'blue']
        ret = {}
        den = [getattr(self, key) for key in _]
        for key in _:
            ret[key] = getattr(self, key) #float(den[key] / sum(den))

        ret['medoid_x'] = self.medoid_x
        ret['medoid_y'] = self.medoid_y
        return ret


pny.sql_debug(False)
db.generate_mapping(check_tables=True, create_tables=True)
