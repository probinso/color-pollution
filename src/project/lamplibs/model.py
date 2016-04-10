#!/usr/bin/env python
import os.path as osp
from   pony.orm import pny
#https://editor.ponyorm.com/user/probinson/lamplibs

from . import utility

DB_LOC = utility.location_resource(fname='index.db')
DBE    = osp.exists(DB_LOC)

db = pny.Database("sqlite", DB_LOC, create_db=True)


class Image(db.Entity):
    id      = pny.PrimaryKey(str)
    type    = pny.Required(str)
    height  = pny.Required(int)
    width   = pny.Required(int)
    derived = pny.Required(bool)

    topograph  = pny.Optional("Topograph", reverse="dst_image")
    top_images = pny.Set("Topograph", reverse="src_image")

    cluster        = pny.Optional("Cluster", reverse="dst_image")
    cluster_images = pny.Set("Cluster", reverse="src_image")


class Topograph(db.Entity):
    dst_image = pny.PrimaryKey(Image, reverse="topograph")
    step      = pny.Required(int)
    src_image = pny.Required(Image, reverse="top_images")


class Cluster(db.Entity):
    dst_image = pny.PrimaryKey(Image, reverse="cluster")
    radius    = pny.Required(int)
    size      = pny.Required(int)
    src_image = pny.Required(Image, reverse="cluster_images")
    lamps     = pny.Set("Lamp")


class Lamp(db.Entity):
    cluster  = pny.Required(Cluster)
    red      = pny.Optional(float)
    green    = pny.Optional(float)
    blue     = pny.Optional(float)
    medoid_x = pny.Required(int)
    medoid_y = pny.Required(int)


pny.sql_debug(True)
pny.db.generate_mapping(check_tables=True, create_tables=True)

