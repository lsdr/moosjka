#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' tracks_to_graph.py - put recent tracks into a graph database '''

__author__ = 'Luiz Rocha'
__version__ = '0.1.0'
__license__ = 'public domain'

from bulbs.model import Node, Relationship
from bulbs.property import String, DateTime
from bulbs.neo4jserver import Graph
from datetime import datetime
from copy import copy

import cPickle as pickle


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

    '''
    as datas do track sao o timestamp em que a musica terminou de ser
    ouvida (e de-facto scrobblada), entao a musica que SEGUIU a musica
    o fez no ts da musica que ANTECEDEU
    
    os arquivos estao em ordem cronologica reversa, ou seja, no track-00001
    a primeira posicao foi a ultima musica capturada (db[0]), a segunda
    posicao (db[1]) foi a musica que ANTECEDEU a db[0].

    entao:
    song_depois = g.song.get_or_create(name=db[0].name, ...)
    song_antes  = g.song.get_or_create(name=db[1].name, ...)
    g.followed.create(db[0], db[1], ts=db[1].ts)
    '''
    db = pickle.load(open('db/tracks-00001.db'))
    add_to_graph(g, db[1], db[0])

 
    # prev=()
    # db_files = glob()
    # for db_file in db_files:
    #     for antes, depois in zip_db(db, prev):
    #         if depois:
    #             add_to_graph(antes, depois)
    #         prev=antes

#
# song_1 = g.song.get_or_create(name='Crackerman', artist='STP')
# song_2 = g.song.get_or_create(name='Dump', artist='Nirvana')
# seq    = g.followed.create(song_2, song_1, ts='1141441596')

