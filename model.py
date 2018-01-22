# -*- coding: utf-8 -*-


class Channel:
    name = None
    source = None
    thumbnail = None
    number = None
    genre = None
    cid = None

    def __init__(self, name, source, thumbnail, number, genre, cid):
        self.name = name
        self.source = source
        self.thumbnail = thumbnail
        self.number = number
        self.genre = genre
        self.cid = cid

class EPG:
    title = None
    descr = None
    next_title = None

    def __init__(self, title, descr, next_title):
        self.descr = descr
        self.title = title
        self.next_title = next_title


