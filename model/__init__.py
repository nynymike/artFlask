from app import db


class SimpleSerializeMixin(object):
    def serialize(self):
        d = {}
        for c in self.__table__.columns:
            v = getattr(self, c.name)
            if v:
                d[c.name] = v
        return d


class Website(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(256))


artwork_websites = db.Table('artwork_websites',
                            db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id')),
                            db.Column('website_name', db.String(128), db.ForeignKey('website.name')))


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
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(256), db.ForeignKey('person.sub'))
    artist = db.relationship('Person', backref='artworks')
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
    # alt_urls = db.relationship('Website', primaryjoin="Artwork.id==AltUrl.artwork_id")
    alt_urls = db.relationship('Website', secondary=artwork_websites)


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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.String(1024))
    picture = db.Column(db.String(256))


person_websites = db.Table('person_websites',
                           db.Column('person_sub', db.String(256), db.ForeignKey('person.sub')),
                           db.Column('website_name', db.String(128), db.ForeignKey('website.name')))


class Person(db.Model, SimpleSerializeMixin):
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
    address = db.Column(db.String(256))
    nickname = db.Column(db.String(64))
    social_urls = db.relationship('Website', secondary=person_websites)
    role = db.Column(db.Enum(['artist', 'staff']))
    twitter = db.Column(db.String(64))
    preferred_contact = db.Column(db.String(256))
    status = db.Column(db.String(64))
    registration_code = db.Column(db.String(64))
    website = db.Column(db.String(256))
    preferred_username = db.Column(db.String(64))
    zoneinfo = db.Column(db.String(256))
    updated_at = db.Column(db.DateTime)
    gender = db.Column(db.String(1))


# class VenueManager(db.Model):
#     venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
#     manager_id = db.Column(db.String(256), db.ForeignKey('person.id'))
    # artist = db.relationship('Person', backref='artworks')


class Medium(db.Model):
    """Primary material used for art"""
    name = db.Column(db.String(128), primary_key=True)
    venue_id = db.Column(db.Integer)


class LimitedVenueTime(db.Model):
    """Used to specify limited hours. List of date and start times"""
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer)


venue_websites = db.Table('venue_websites',
                          db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
                          db.Column('website_name', db.String(128), db.ForeignKey('website.name')))


venue_artists = db.Table('venue_artists',
                         db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
                         db.Column('artist_id', db.String(256), db.ForeignKey('person.sub')))

venue_managers = db.Table('venue_managers',
                          db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')),
                          db.Column('manager_id', db.String(256), db.ForeignKey('person.sub')))


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
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(256))
    event_id = db.Column(db.Integer)
    event = db.relationship('Event')
    picture = db.Column(db.String(256))
    address = db.Column(db.String(256))
    # coordinates
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    twitter = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    category = db.Column(db.String(128))
    mediums = db.relationship('Medium')
    description = db.Column(db.String(1024))
    artists = db.relationship('Person', secondary=venue_artists)
    websites = db.relationship('Website', secondary=venue_websites)
    managers = db.relationship('Person', secondary=venue_managers)
    curated = db.Column(db.Boolean)
    # limited times
    times = db.relationship('LimitedVenueTime')
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
