"""
.. currentmodule:: model.Art

Art Entity Schema
-----------------

+-------------+--------------+------------------------------------------------------------------------+
| member      | type         | description                                                            |
+=============+==============+========================================================================+
| id          | string       | unique identifier for the work                                         |
+-------------+--------------+------------------------------------------------------------------------+
| artist      | string       | artist id                                                              |
+-------------+--------------+------------------------------------------------------------------------+
| title       | string       | Title for the work                                                     |
+-------------+--------------+------------------------------------------------------------------------+
| description | string       | Artwork materials and style                                            |
+-------------+--------------+------------------------------------------------------------------------+
| picture     | string       | URI for a jpg of artwork                                               |
+-------------+--------------+------------------------------------------------------------------------+
| thumbnail   | string       | URL for a tiny  version of the jpg                                     |
+-------------+--------------+------------------------------------------------------------------------+
| buyURL      | string       | URL for website to buy the work                                        |
+-------------+--------------+------------------------------------------------------------------------+
| venue       | string       | Venue id                                                               |
+-------------+--------------+------------------------------------------------------------------------+
| medium      | string       | Artwork materials and style                                            |
+-------------+--------------+------------------------------------------------------------------------+
| sold_out    | boolean      | All works in this series are sold                                      |
+-------------+--------------+------------------------------------------------------------------------+
| series      | List<string> | List of Art IDs for related works                                      |
+-------------+--------------+------------------------------------------------------------------------+
| parent_work | string       | Art ID of work that is the parent, or provides some other context      |
+-------------+--------------+------------------------------------------------------------------------+
| size        | string       | Size of the work                                                       |
+-------------+--------------+------------------------------------------------------------------------+
| year        | string       | Year the work was created                                              |
+-------------+--------------+------------------------------------------------------------------------+
| alt_urls    | List<string> | Dictionary of alternate sites: name:url                                |
+-------------+--------------+------------------------------------------------------------------------+

Art Entity JSON sample:
-----------------------

.. code-block:: javascript

        {
        'id': '1d5bfb0f-8c4b-11e3-b767-3c970e1b8563',
        'artist': '3ad50b37-947e-46f6-940c-44804d95304f',
        'title': 'Austin Sunrise',
        'description': 'Third in a series of 90 painting of the beautiful Austin skyline',
        'picture': 'http://artFlask.us/api/v1/art/140a3bfc-63a4-4f88-9d63-893e69f88890',
        'thumbnail': 'http://artFlask.us/api/v1/art/140a3bfc-63a4-4f88-9d63-893e69f88890?thumbnail=true'
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

import json

class ArtWork():

    _collection_ = "ArtWork"

    schema =  {
        # 'id': {type:'str'},
        'artist': {type:'str'},
        'title': {type:'str'},
        'description': {type:'str'},
        'picture': {type:'str'},
        'thumbnail': {type:'str'},
        'buyURL': {type:'str'},
        'venue': {type:'str'},
        'medium': {type:'str'},
        'sold_out': {type:'str'},
        'series': {type:'List'},
        'parent_work': {type:'str'},
        'size': {type:'str'},
        'year': {type:'str'},
        'alt_urls': {type:'List'}
        }


    def __init__(self):
        # self.id = ""
        self.artist = ""
        self.title = ""
        self.description = ""
        self.picture = ""
        self.thumbnail = ""
        self.buyURL = ""
        self.venue = ""
        self.medium = ""
        self.sold_out = False
        self.series = []
        self.parent_work = ''
        self.size = ''
        self.year = ''
        self.alt_urls = {}

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        # if self.not_empty(self.id): d['id'] = self.id
        if self.not_empty(self.artist): d['artist'] = self.artist
        if self.not_empty(self.title): d['title'] = self.title
        if self.not_empty(self.description): d['description'] = self.description
        if self.not_empty(self.picture): d['picture'] = self.picture
        if self.not_empty(self.thumbnail): d['thumbnail'] = self.thumbnail
        if self.not_empty(self.buyURL): d['buyURL'] = self.buyURL
        if self.not_empty(self.venue): d['venue'] = self.venue
        if self.not_empty(self.medium): d['medium'] = self.medium
        if self.not_empty(self.parent_work): d['parent_work'] = self.parent_work
        if self.not_empty(self.size): d['size'] = self.size
        if self.not_empty(self.year): d['year'] = self.year
        if self.series: d['series'] = self.series
        d['sold_out'] = self.sold_out
        if self.alt_urls: d['alt_urls'] = self.alt_urls
        return json.dumps(d)
    
    def to_dict(self):
        d = {}
        # if self.not_empty(self.id): d['id'] = self.id
        if self.not_empty(self.artist): d['artist'] = self.artist
        if self.not_empty(self.title): d['title'] = self.title
        if self.not_empty(self.description): d['description'] = self.description
        if self.not_empty(self.picture): d['picture'] = self.picture
        if self.not_empty(self.thumbnail): d['thumbnail'] = self.thumbnail
        if self.not_empty(self.buyURL): d['buyURL'] = self.buyURL
        if self.not_empty(self.venue): d['venue'] = self.venue
        if self.not_empty(self.medium): d['medium'] = self.medium
        if self.not_empty(self.parent_work): d['parent_work'] = self.parent_work
        if self.not_empty(self.size): d['size'] = self.size
        if self.not_empty(self.year): d['year'] = self.year
        if self.series: d['series'] = self.series
        d['sold_out'] = self.sold_out
        if self.alt_urls: d['alt_urls'] = self.alt_urls
        return d