# -*- coding: utf-8 -*-
import urllib2


def request(url, data):
    req = urllib2.Request(url, data)
    req.add_header('Content-type', 'application/xml')
    req.add_header('Content-Length', str(len(data)))
    resp = urllib2.urlopen(req)
    return resp.read()
