from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import db

# __author__ = 'mike'
# from Art import ArtWork
# from Event import Event
# from Person import Person
# from Venue import Venue


# 'artist': {type : str},
# 'title': {type : str},
# 'description': {type : str},
# 'picture': {type : str},
# 'thumbnail': {type : str},
# 'buyURL': {type : str},
# 'venue': {type : str},
# 'medium': {type : str},
# 'sold_out': {type : bool},
# 'series': {type : list},
# 'parent_work': {type : str},
# 'size': {type:str},
# 'year': {type : str},
# 'alt_urls': {type : dict}


# app = Flask(__name__)


class AltUrl(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(256))


class Artwork(db.Model):
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
    alt_urls = db.relationship('AltUrl')
