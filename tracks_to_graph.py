#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' tracks_to_graph.py - put recent tracks into a graph database '''

__author__ = 'luiz rocha'
__version__ = '0.1.0'
__license__ = 'public domain'

from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime

class Song(Node):
    element_type = 'song'
    # attributes
    name    = String(nullable=False)
    artist  = String(nullable=False)
    url     = String(nullable=True)


class Followed(Relationship):
    label = 'followed'
    # attributes
    ts = DateTime(nullable=False)



# from bulbs.neo4jserver import Graph
#
# g = Graph()
# g.add_proxy('song', Song)
# g.add_proxy('followed', Followed)
#
# song_1 = g.song.get_or_create(name='Crackerman', artist='STP')
# song_2 = g.song.get_or_create(name='Dump', artist='Nirvana')
# seq    = g.followed.create(song_2, song_1, ts='1141441596')

