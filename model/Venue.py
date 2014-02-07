"""
.. currentmodule:: model.Venue

Venue Entity Schema
-------------------

+-------------+---------------+------------------------------------------------------------------------+
| member      | type          | description                                                            |
+=============+===============+========================================================================+
| id          | string        | unique identifier for the venue                                        |
+-------------+---------------+------------------------------------------------------------------------+
| name        | string        | Name of the venue - MUST be unique                                     |
+-------------+---------------+------------------------------------------------------------------------+
| event_id    | string        | Event id                                                               |
+-------------+---------------+------------------------------------------------------------------------+
| picture     | string        | URL of the End-User's profile picture. This URL MUST refer to an image |
|             |               | file (for example, a PNG, JPEG, or GIF image file), rather than to a   |
|             |               | Web page containing an image.                                          |
+-------------+---------------+------------------------------------------------------------------------+
| address     | string        | Address as defined in                                                  |
|             |               | http://openid.net/specs/openid-connect-core-1_0.html#AddressClaim      |
+-------------+---------------+------------------------------------------------------------------------+
| coordinates | string        | List of the North-South decimal values, where North and East  are      |
|             |               | positive, and South and West are negative                              |
+-------------+---------------+------------------------------------------------------------------------+
| twitter     | string        | Twitter handle for the venue                                           |
+-------------+---------------+------------------------------------------------------------------------+
| mail        | string        | Email address for venue                                                |
+-------------+---------------+------------------------------------------------------------------------+
| phone       | string        | Phone number for venue                                                 |
+-------------+---------------+------------------------------------------------------------------------+
| category    | string        | i.e. "Happenings", "Exhibitions" or  "Artists & Studios"               |
+-------------+---------------+------------------------------------------------------------------------+
| medium      | string        | Primary material used for art                                          |
+-------------+---------------+------------------------------------------------------------------------+
| description | string        | Brief text about the venue                                             |
+-------------+---------------+------------------------------------------------------------------------+
| artists     | List<string>  | Person IDs authorized to post work to this venue                       |
+-------------+---------------+------------------------------------------------------------------------+
| websites    | List<string>  | List of URLs for the venue's websites                                  |
+-------------+---------------+------------------------------------------------------------------------+
| managers    | List<string>  | Person IDs authorized to manage the venue                              |
+-------------+---------------+------------------------------------------------------------------------+
| ad_1        | Boolean       | Parking: Official parking for the disabled                             |
+-------------+---------------+------------------------------------------------------------------------+
| ad_2        | Boolean       | Entrance and interior: Minimum 32" doorway clearance space             |
+-------------+---------------+------------------------------------------------------------------------+
| ad_3        | Boolean       | Entrance and interior: Entry way without stairs, no lip & with a ramp  |
+-------------+---------------+------------------------------------------------------------------------+
| ad_4        | Boolean       | Entrance and interior: Path around studio with minimum 36" width       |
+-------------+---------------+------------------------------------------------------------------------+
| ad_5        | Boolean       | Restrooms: Entry way with minimum 36" wide clearance space             |
+-------------+---------------+------------------------------------------------------------------------+
| ad_6        | Boolean       | Restrooms: Minimum 56x60 inch clearance space for toilet               |
+-------------+---------------+------------------------------------------------------------------------+
| ad_7        | Boolean       | Restrooms: Grab bars                                                   |
+-------------+---------------+------------------------------------------------------------------------+
| ad_8        | Boolean       | Other: Braille or raised letter signage                                |
+-------------+---------------+------------------------------------------------------------------------+


Venue Entity JSON sample:
-------------------------

.. code-block:: javascript

        {
        'id': 'd471b627-f7f3-4872-96e2-2af4d813673f',
        'name': 'Gallery Happy',
        'evemt_id': 'a93335d9-ca6e-4824-8e30-fdd4551d2c7b',
        'picture': 'http://www.galleryhappy.com/logo.png'
        'address': '100 Cesar Chavez\\nAustin, TX 78702'
        'coordinates': ['40.446195', '-79.982195'],
        'twitter': '@GalleryHappy',
        'mail':'info@galleryhappy.org',
        'phone':'+1 512-555-1212',
        'category':'Artists & Studios'.
        'medium':'Ceramics',
        'description':'Fun stuff made of clay by talented people.',
        'artists': ['b18af90a-4054-4c13-a382-8987bbaeb58b'],
        'websites': ['http://www.galleryhappy.com'],
        'managers': ['c3491f70-8c92-11e3-a91c-3c970e1b8563'],
        ad_1: true,
        ad_2: true,
        ad_3: true,
        ad_4: true,
        ad_5: true,
        ad_6: true,
        ad_7: true,
        ad_8: false
        }

"""
import sys

class Venue():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.event_id = ""
        self.picture = ""
        self.address = ""
        self.coordinates = ""
        self.twitter = ""
        self.mail = ""
        self.phone = ""
        self.category = ""
        self.medium = ""
        self.description = ""
        self.artists = []
        self.websites = []
        self.managers = []
        self.ada_1 = False
        self.ada_2 = False
        self.ada_3 = False
        self.ada_4 = False
        self.ada_5 = False
        self.ada_6 = False
        self.ada_7 = False
        self.ada_8 = False

def not_empty(self, s):
    if type(s) == type(""):
        if s != "": return True
        return False

def get_boolean(b):
    if b: return "true"
    return "false"

def __str__(self):
    d = {}
    if self.not_empty(self.id): d['id'] = self.id
    if self.not_empty(self.name): d['name'] = self.name
    if self.not_empty(self.event_id): d['event_id'] = self.event_id
    if self.not_empty(self.picture): d['picture'] = self.picture
    if self.not_empty(self.address): d['address'] = self.address
    if self.not_empty(self.coordinates): d['coordinates'] = self.coordinates
    if self.not_empty(self.twitter): d['twitter'] = self.twitter
    if self.not_empty(self.mail): d['mail'] = self.mail
    if self.not_empty(self.phone): d['phone'] = self.phone
    if self.not_empty(self.category): d['category'] = self.twitter
    if self.not_empty(self.medium): d['medium'] = self.medium
    if self.not_empty(self.description): d['description'] = self.description
    if len(self.artists): d['artists'] = self.artists
    if len(self.websites): d['websites'] = self.websites
    if len(self.managers): d['managers'] = self.managers
    self['ad_1'] = get_boolean(self.ad_1)
    self['ad_2'] = get_boolean(self.ad_2)
    self['ad_3'] = get_boolean(self.ad_3)
    self['ad_4'] = get_boolean(self.ad_4)
    self['ad_5'] = get_boolean(self.ad_5)
    self['ad_6'] = get_boolean(self.ad_6)
    self['ad_7'] = get_boolean(self.ad_7)
    self['ad_8'] = get_boolean(self.ad_8)
    return str(d)
