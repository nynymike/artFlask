import json

from app import db

# from Art import ArtWork
# from Event import Event
# from Person import Person
# from Venue import Venue


class SimpleSerializeMixin:
    def serialize(self):
        d = {}
        for c in self.__table__.columns:
            v = getattr(self, c.name)
            if v:
                d[c.name] = v
        return d


class AltUrl(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(256))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))


class Artwork(db.Model, SimpleSerializeMixin):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    picture = db.Column(db.String(256))
    thumbnail = db.Column(db.String(256))
    buyurl = db.Column(db.String(256))
    venue = db.Column(db.String(256))
    medium = db.Column(db.String(256))
    sold_out = db.Column(db.Boolean)
    series = db.relationship('Artwork')
    parent_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))
    parent = db.relationship('Artwork', remote_side=[id])
    size = db.Column(db.String(256))
    year = db.Column(db.Integer)
    alt_urls = db.relationship('AltUrl', primaryjoin="Artwork.id==AltUrl.artwork_id")