# -*- coding: utf-8 -*-"""
"""
This module describes the Model in our Model View Controller.
"""

import os.path  as osp
import pony.orm as pny

from  shutil    import copy
from .utility   import get_resource, ptrace
from .lamplight import image_info

'https://editor.ponyorm.com/user/probinson/lamplibs'

from . import utility

DB_LOC = utility.location_resource(fname='index.db')
DBE    = osp.exists(DB_LOC)

db = pny.Database("sqlite", DB_LOC, create_db=True)


class Image(db.Entity):
    _table_ = "tbl_image"
    id      = pny.PrimaryKey(str)
    type    = pny.Required(str)
    height  = pny.Required(int)
    width   = pny.Required(int)
    derived = pny.Required(bool)

    topograph  = pny.Optional("Topograph", reverse="dst_image")
    top_images = pny.Set("Topograph", reverse="src_image")

    cluster        = pny.Optional("Cluster", reverse="dst_image")
    cluster_images = pny.Set("Cluster", reverse="src_image")

    @property
    def data(self):
        *_, data = image_info(get_resource(self.id))
        return data



@ptrace
@pny.db_session
def retrieve_image(resource, destination, rename='output'):
    img = Image.get(id=resource)
    if not img:
        raise FileNotFoundError("database resource '{}'".format(resource))
    savename = rename + '.' + img.type
    copy(get_resource(resource), osp.join(destination, savename))


class Topograph(db.Entity):
    _table_   = "tbl_topograph"
    dst_image = pny.PrimaryKey(Image, reverse="topograph")
    step      = pny.Required(int)
    src_image = pny.Required(Image, reverse="top_images")


class Cluster(db.Entity):
    _table_   = "tbl_cluster"
    dst_image = pny.PrimaryKey(Image, reverse="cluster")
    radius    = pny.Required(int)
    size      = pny.Required(int)
    src_image = pny.Required(Image, reverse="cluster_images")
    lamps     = pny.Set("Lamp")


class Lamp(db.Entity):
    _table_  = "tbl_lamp"
    cluster  = pny.Required(Cluster)
    red      = pny.Optional(float)
    green    = pny.Optional(float)
    blue     = pny.Optional(float)
    medoid_x = pny.Required(int)
    medoid_y = pny.Required(int)


# pny.sql_debug(True)
db.generate_mapping(check_tables=True, create_tables=True)
