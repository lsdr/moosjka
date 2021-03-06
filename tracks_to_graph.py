#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' tracks_to_graph.py - put recent tracks into a graph database '''

__author__ = 'Luiz Rocha'
__version__ = '0.1.0'
__license__ = 'public domain'

from progressbar import Bar, Percentage, ProgressBar
from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime
from bulbs.neo4jserver import Graph
from datetime import datetime
from glob import glob
from copy import copy

import cPickle as pickle

WIDGETS = [Percentage(), ' ', Bar()]

class Song(Node):
    element_type = 'song'
    # attributes
    name    = String(nullable=False)
    artist  = String(nullable=False)
    url     = String(nullable=True)


class FollowedBy(Relationship):
    label = 'followed_by'
    # attributes
    ts = DateTime(nullable=False)


def add_to_graph(graph, antes, depois):
    song_antes  = add_song(graph, antes)
    song_depois = add_song(graph, depois)

    ts = datetime.fromtimestamp(int(antes[3]))
    graph.followed_by.create(song_antes, song_depois, ts=ts)


def add_song(graph, song):
    artist, name, url, ts = song
    record = graph.song.get_or_create('name', name, name=name, artist=artist, url=url)
    return record


def zip_db(db, prev=()):
    _tmp_db = copy(db)
    _tmp_db.insert(0, prev)
    _tmp_db.pop()
    return zip(db, _tmp_db)


if __name__ == '__main__':
    g = Graph()
    g.add_proxy('song', Song)
    g.add_proxy('followed_by', FollowedBy)

    # db = pickle.load(open('db/tracks-00001.db'))
    # add_to_graph(g, db[1], db[0])

    prev=()
    db_files = glob('db/tracks*')

    for db_file in db_files:
        print 'processing %s file right now...' % db_file 
        db   = pickle.load(open(db_file))
        pbar = ProgressBar(widgets=WIDGETS, maxval=200).start()
        for i, (antes, depois) in enumerate(zip_db(db, prev)):
            if depois:
                add_to_graph(g, antes, depois)
            pbar.update(i+1)
        prev=antes
        pbar.finish()

