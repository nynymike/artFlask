import json
import hashlib
from datetime import datetime as dtime, date

from app import db


class SimpleSerializeMixin(object):
    def as_dict(self, include_id=False):
        d = {}
        for c in self.__table__.columns:
            v = getattr(self, c.name)
            # ignore
            if (include_id or c.name != 'id') and v:
                if isinstance(v, dtime):
                    v = v.strftime("%c")
                elif isinstance(v, date):
                    v = v.strftime('%a %b %d %Y')
                d[c.name] = v
        return d


class JsonModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SimpleSerializeMixin):
            return obj.as_dict()
        return super(JsonModelEncoder, self).default(obj)


class RegistrationCode(db.Model, SimpleSerializeMixin):
    __tablename__ = "registration_codes"

    id = db.Column(db.Integer, primary_key=True)
    accepted = db.Column(db.DateTime, nullable=True)
    sent = db.Column(db.DateTime, nullable=True)

    def hashed_id(self):
        return hashlib.sha224(str(self.id)).hexdigest()

    def as_dict(self, include_id=False):
        d = super(RegistrationCode, self).as_dict(False)
        return {
            self.hashed_id(): d,
        }


class Website(db.Model, SimpleSerializeMixin):
    __tablename__ = "websites"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    url = db.Column(db.String(256))


class Address(db.Model, SimpleSerializeMixin):
    __tablename__ = "physical_addresses"

    id = db.Column(db.Integer(), primary_key=True)
    street = db.Column(db.String(128))
    locality = db.Column(db.String(64))
    region = db.Column(db.String(64))
    postal_code = db.Column(db.Integer)
    country = db.Column(db.String(64))


person_websites = db.Table('person_websites',
                           db.Column('person_sub', db.String(256), db.ForeignKey('persons.sub')),
                           db.Column('website_id', db.String(128), db.ForeignKey('websites.id')))


class Person(db.Model, SimpleSerializeMixin):
    __tablename__ = "persons"

    # OpenID Connect identifier, 256 should be enough for max len
    sub = db.Column(db.String(256), primary_key=True)
    given_name = db.Column(db.String(64))
    family_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    birthdate = db.Column(db.Date)
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    picture = db.Column(db.String(256))
    phone_number_verified = db.Column(db.Boolean, default=False)
    address_id = db.Column(db.Integer, db.ForeignKey('physical_addresses.id'))
    address = db.relationship(Address, uselist=False)
    nickname = db.Column(db.String(64))
    social_urls = db.relationship('Website', secondary=person_websites)
    role = db.Column(db.Enum('artist', 'staff'))
    twitter = db.Column(db.String(64))
    preferred_contact = db.Column(db.String(256))
    status = db.Column(db.String(64))
    registration_code_id = db.Column(db.Integer, db.ForeignKey('registration_codes.id'))
    registration_code = db.relationship('RegistrationCode')
    website_id = db.Column(db.Integer, db.ForeignKey('websites.id'))
    website = db.relationship('Website')
    preferred_username = db.Column(db.String(64))
    zoneinfo = db.Column(db.String(256))
    updated_at = db.Column(db.DateTime)
    gender = db.Column(db.String(1))

    def as_dict(self, include_id=False):
        d = super(Person, self).as_dict(include_id)
        if 'address_id' in d:
            del d['address_id']
            d['address'] = self.address.as_dict()
        if 'registration_code_id' in d:
            del d['registration_code_id']
            d['registration_code'] = self.registration_code.as_dict()
        if 'website_id' in d:
            del d['website_id']
            d['website'] = self.website.as_dict()
        d['social_urls'] = [u.as_dict() for u in self.social_urls]
        return d


artwork_websites = db.Table(
    'artwork_websites',
    db.Column('artwork_id', db.Integer, db.ForeignKey('artworks.id')),
    db.Column('website_id', db.String(128), db.ForeignKey('websites.id'))
)


class Event(db.Model, SimpleSerializeMixin):
    """
    {
        'id': 'happy2014',
        'name': 'Happy Tour 2014',
        'startDate': 'Feb  3 00:00:00 UTC 2014',
        'endDate': 'Feb  5 00:00:00 UTC 2014',
        'description': 'This is a tour of all the artwork that you would want to see to make you smile',
        'picture': 'http://happytour.org/happy2014.png'
    }
    """
    __tablename__ = "art_events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.String(1024))
    picture = db.Column(db.String(256))


class Medium(db.Model):
    """Primary material used for art"""

    __tablename__ = "mediums"

    name = db.Column(db.String(128), primary_key=True)


class LimitedTime(db.Model):
    """Used to specify limited hours. List of date and start times"""
    __tablename__ = "limitation_time"

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)


venue_mediums = db.Table('venue_mediums',
                         db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                         db.Column('medium_name', db.String(128), db.ForeignKey('mediums.name')))


venue_artists = db.Table('venue_artists',
                         db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                         db.Column('artist_id', db.String(256), db.ForeignKey('persons.sub')))


venue_websites = db.Table('venue_websites',
                          db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                          db.Column('website_name', db.String(128), db.ForeignKey('websites.name')))


venue_managers = db.Table('venue_managers',
                          db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                          db.Column('manager_id', db.String(256), db.ForeignKey('persons.sub')))

venue_limited_time = db.Table('venue_limited_time',
                              db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                              db.Column('time_id', db.Integer, db.ForeignKey('limitation_time.id')))


class Venue(db.Model, SimpleSerializeMixin):
    """
    'id': 'd471b627-f7f3-4872-96e2-2af4d813673f',
    'site_id': '101c',
    'name': 'Gallery Happy',
    'event_id': 'happy2014',
    'picture': 'http://www.galleryhappy.com/logo.png'
    'address': {"street_address": "621 East Sixth Street",
                "locality": "Austin",
                "region": "TX",
                "postal_code": "78701",
                "country": "US"},
    '100 Cesar Chavez\\nAustin, TX 78702'
    'coordinates': ['40.446195', '-79.982195'],
    'twitter': '@GalleryHappy',
    'mail':'info@galleryhappy.org',
    'phone':'+1 512-555-1212',
    'category':'Artists & Studios'.
    'mediums': ['Ceramics'],
    'description':'Fun stuff made of clay by talented people.',
    'artists': ['b18af90a-4054-4c13-a382-8987bbaeb58b'],
    'websites': ['http://www.galleryhappy.com'],
    'managers': ['c3491f70-8c92-11e3-a91c-3c970e1b8563'],
    'curated': true,
    'times': ['Feb  3 12:00:00 UTC 2014', 'Feb  3 14:00:00 UTC 2014']
    ...

    """
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(256))
    event_id = db.Column(db.Integer, db.ForeignKey('art_events.id'))
    event = db.relationship('Event')
    picture = db.Column(db.String(256))
    address_id = db.Column(db.Integer, db.ForeignKey('physical_addresses.id'))
    address = db.relationship(Address, uselist=False)
    # coordinates
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    twitter = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    category = db.Column(db.String(128))
    mediums = db.relationship('Medium', secondary=venue_mediums)
    description = db.Column(db.String(1024))
    artists = db.relationship('Person', secondary=venue_artists)
    websites = db.relationship('Website', secondary=venue_websites)
    managers = db.relationship('Person', secondary=venue_managers)
    curated = db.Column(db.Boolean)
    # limited times
    times = db.relationship('LimitedTime', secondary=venue_limited_time)
    # Parking: Official parking for the disabled
    ad_1 = db.Column(db.Boolean)
    # Entrance and interior: Minimum 32" doorway clearance space
    ad_2 = db.Column(db.Boolean)
    # Entrance and interior: Entry way without stairs, no lip & with a ramp
    ad_3 = db.Column(db.Boolean)
    # Entrance and interior: Path around studio with minimum 36" width
    ad_4 = db.Column(db.Boolean)
    # Restrooms: Entry way with minimum 36" wide clearance space
    ad_5 = db.Column(db.Boolean)
    # Restrooms: Minimum 56x60 inch clearance space for toilet
    ad_6 = db.Column(db.Boolean)
    # Restrooms: Grab bars
    ad_7 = db.Column(db.Boolean)
    # Other: Braille or raised letter signage
    ad_8 = db.Column(db.Boolean)

    def as_dict(self, include_id=False):
        d = super(Venue, self).as_dict()
        if 'event_id' in d:
            del d['event_id']
            d['event'] = self.event_id
        if 'address_id' in d:
            del d['address_id']
            d['address'] = self.address.as_dict()
        d['mediums'] = [m.name for m in self.mediums]
        d['artists'] = [a.sub for a in self.artists]
        d['websites'] = [w.url for w in self.websites]
        d['managers'] = [m.sub for m in self.managers]
        d['times'] = [t.start.strftime("%c") for t in self.times]
        return d


class Artwork(db.Model, SimpleSerializeMixin):
    """
        {
        'id': '1d5bfb0f-8c4b-11e3-b767-3c970e1b8563',
        'artist': '3ad50b37-947e-46f6-940c-44804d95304f',
        'title': 'Austin Sunrise',
        'description': 'Third in a series of 90 painting of the beautiful Austin skyline',
        'buyURL': 'http://auction.com/item/3432840932',
        'venue': '37ae018a-1fb2-4da0-8b75-e439c92e6dd5',
        'medium': 'Painting',
        'sold_out': 'false'
        'series': ['cd32b78b-55c5-4e1f-a482-55669f3b466b',
                   'dc7a61e5-06ff-481c-9037-6d82485a47af'],
        'parent_work': '237747c7-58bd-4822-a577-992714ebadf7'
        'size': '24"x34"',
        'year': '2014',
        'alt_urls': {'Detail':'http://goo.gl/23A3fi', 'Back':'http://goo.gl/xc3wyo',}
        }
    """
    __tablename__ = "artworks"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(256), db.ForeignKey('persons.sub'))
    artist = db.relationship('Person', backref='artworks')
    title = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    picture = db.Column(db.String(256))
    thumbnail = db.Column(db.String(256))
    buy_url = db.Column(db.String(256))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    venue = db.relationship('Venue', uselist=False)
    medium = db.Column(db.String(256))
    sold_out = db.Column(db.Boolean)
    series = db.relationship('Artwork')
    parent_id = db.Column(db.Integer, db.ForeignKey('artworks.id'))
    parent_work = db.relationship('Artwork', backref='children', remote_side=[id])
    # size = db.Column(db.String(256))
    height = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer)
    alt_urls = db.relationship('Website', secondary=artwork_websites)

    def as_dict(self, include_id=False):
        d = super(Artwork, self).as_dict()
        d['artist'] = self.artist_id
        d['venue'] = self.venue_id
        d['parent_work'] = self.parent_id
        d['alt_urls'] = {}
        for u in self.alt_urls:
            d['alt_urls'][u.name] = u.url
        if not d.get('series'):
            d['series'] = []

        return d
