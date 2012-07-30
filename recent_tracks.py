#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from bulbs.model import Node, Relationship
# from bulbs.property import String, Integer, DateTime
# from bulbs.utils import current_datetime

from lastfm import LastFM
import cPickle as pickle

# class Person(Node):
#     element_type = "person"
#     name = String(nullable=False)
#     age = Integer()
#        
# 
# class Knows(Relationship):
#     label = "knows"
#     created = DateTime(default=current_datetime, nullable=False)
#

def extractTrackData(track):
    _data = (track.findtext('artist'), track.findtext('name'),
             track.findtext('url'), track.find('date').get('uts'))
    return _data

def isLastPage(track):
    current = int(tracks.find('recenttracks').get('page'))
    total   = int(tracks.find('recenttracks').get('totalPages'))
    return current == total

def itertracks(tracks):
    return (t for t in tracks.findall('recenttracks/track') if t.get('nowplaying') is None)


if __name__ == '__main__':
    service = LastFM('7cc9edbf1289e55d01f6d0b6a6fd159b', 'lsdr')

    print 'processing page 1'
    tracks = service.fetch('user.getrecenttracks', limit='100', page='1')
    data   = [extractTrackData(t) for t in itertracks(tracks)]
    pages  = tracks.find('recenttracks').get('totalPages')
    # print data
    # print pages
    # print

    for i in xrange(2, int(pages)+1):
        print 'processing page %s now' % str(i)
        tracks = service.fetch('user.getrecenttracks', limit='100', page=str(i))
        data  += [extractTrackData(t) for t in itertracks(tracks)]
        # print data
    
    with open('tracks.db', 'w+') as db:
        pickle.dump(data, db)
        db.close()

    
'''
# Tratando o UTS timestamp
__timestamp_tuple = time.gmtime(float(UTS))
__timestamp = time.time.asctime(__timestamp_tuple)
print __timestamp
>> 'Thu Apr  5 16:36:05 2012'

# Processo de importação
<recenttracks user="lsdr" page="1" perPage="100" totalPages="520" total="51914">

# Uso do Pickle:
200 tracks  =>  24 Kb (~  24576 bytes)
1000 tracks => 115 Kb (~ 117760 bytes)
2000 tracks => 230 Kb (~ 235520 bytes)
5000 tracks => 578 Kb (~ 591872 bytes)

5x o número de tracks, 4.79x o número de bytes
10x o número de tracks, 9.58x o número de bytes
25x o número de tracks, 24.08x o número de bytes

em tese, crescimento linear (~ 123 bytes/track) logo, para 
51.914 tracks (em 08/04), db seria aprox. 6 Mb.

# Ler o DB:
    from cPickle import load
    with open('tracks.db') as f:
        data = load(f)
        
    len(data)

# Benchmark:
time ./recent_tracks.py (com 50 fetches, 100 tracks/fetch)

    real	0m59.470s
    user	0m0.581s
    sys     0m0.166s

1m é 1/10 do tempo que vai ser necessário -- de acordo com o benchmark, ou seja,
o processo inteiro deve demorar uns 10 minutos.
'''
