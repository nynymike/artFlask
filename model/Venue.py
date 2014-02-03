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
| artists     | List<string>  | Person IDs authorized to post work to this venue                       |
+-------------+---------------+------------------------------------------------------------------------+
| websites    | List<string>  | List of URLs for the venue's websites                                  |
+-------------+---------------+------------------------------------------------------------------------+
| managers    | List<string>  | Person IDs authorized to manage the venue                              |
+-------------+---------------+------------------------------------------------------------------------+

Venue Entity JSON sample:
-------------------------

.. code-block:: javascript

        {
        'id': '6ed666a3-4461-4451-b58e-74adf3e76902',
        'name': 'Gallery Happy',
        'picture': 'http://www.galleryhappy.com/logo.png'
        'address': '100 Cesar Chavez\\nAustin, TX 78702'
        'coordinates': ['40.446195', '-79.982195'],
        'twitter': "@GalleryHappy",
        'artists': ['b18af90a-4054-4c13-a382-8987bbaeb58b'],
        'websites': ['http://www.galleryhappy.com'],
        'managers': ['c3491f70-8c92-11e3-a91c-3c970e1b8563']
        }

"""
import sys

class ArtWork():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.picture = ""
        self.address = ""
        self.coordinates = ""
        self.twitter = ""
        self.artists = []
        self.websites = []
        self.managers = []

def not_empty(self, s):
    if type(s) == type(""):
        if s != "": return True
        return False
    elif type(s) == type([]):
        if len(s) > 0: return True
        return False
    sys.exit(-1)

def __str__(self):
    d = {}
    if self.not_empty(self.id): d['id'] = self.id
    if self.not_empty(self.name): d['name'] = self.name
    if self.not_empty(self.picture): d['picture'] = self.picture
    if self.not_empty(self.address): d['address'] = self.address
    if self.not_empty(self.coordinates): d['coordinates'] = self.coordinates
    if self.not_empty(self.twitter): d['twitter'] = self.twitter
    if self.not_empty(self.artists): d['artists'] = self.artists
    if self.not_empty(self.websites): d['websites'] = self.websites
    if self.not_empty(self.managers): d['managers'] = self.managers
    return str(d)
