# -*- coding: utf-8 -*-
''' lastfm.py - LastFM API dense client '''

__author__ = 'Luiz Rocha'
__version__ = '0.1.0'
__license__ = "public domain"

# from urllib.parse import urlencode
from urllib import urlencode
from httplib2 import Http
from xml.etree import cElementTree as ElementTree
from sys import exit

API_ROOT = 'http://ws.audioscrobbler.com/2.0/'

class LastFM:
    def __init__(self, token, user):
        self.conn = Http('.cache')
        self.credentials = dict(
            api_key = token,
            user    = user)
    
    def buildURL(self, **kwargs):
        return "%s?%s" % (API_ROOT, urlencode(kwargs))

    def parseXML(self, body):
        xml = ElementTree.XML(body)
        return xml

    def fetch(self, method, *args, **kwargs):
        kw = dict(method=method)
        kw.update(self.credentials)
        kw.update(kwargs)
        
        request_url = self.buildURL(**kw)
        print(request_url)
        header, body = self.conn.request(request_url, 'GET')
        if header.status == 200:
            return self.parseXML(body)
        else:
            # 403, 503
            print(header)
            print(body)
            exit(1)

