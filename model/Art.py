"""
.. currentmodule:: model.Art

Art Entity Schema
-----------------

+-------------+------------+------------------------------------------------------------------------+
| member      | type       | description                                                            |
+=============+============+========================================================================+
| id          | string     | unique identifier for the work                                         |
+-------------+------------+------------------------------------------------------------------------+
| artist      | string     | artist id                                                              |
+-------------+------------+------------------------------------------------------------------------+
| title       | string     | Title for the work                                                     |
+-------------+------------+------------------------------------------------------------------------+
| description | string     | Artwork materials and style                                            |
+-------------+------------+------------------------------------------------------------------------+
| picture     | string     | URI for a jpg of artwork                                               |
+-------------+------------+------------------------------------------------------------------------+
| thumbnail   | string     | URI for a tiny  version of the jpg                                     |
+-------------+------------+------------------------------------------------------------------------+
| ebay        | string     | URI for ebay auction                                                   |
+-------------+------------+------------------------------------------------------------------------+
| venue       | string     | Venue id                                                               |
+-------------+------------+------------------------------------------------------------------------+
| medium      | string     | Artwork materials and style                                            |
+-------------+------------+------------------------------------------------------------------------+
| sold        | boolean    | Whether artwork is sold                                                |
+-------------+------------+------------------------------------------------------------------------+

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
        'ebay': 'http://auction.com/item/3432840932',
        'venue': '37ae018a-1fb2-4da0-8b75-e439c92e6dd5',
        'medium': 'Painting',
        'sold': 'false'
        }

"""
class ArtWork():
    def __init__(self):
        self.id = ""
        self.artist = ""
        self.title = ""
        self.description = ""
        self.picture = ""
        self.thumbnail = ""
        self.ebay = ""
        self.venue = ""
        self.medium = ""
        self.sold = False

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        if self.not_empty(self.id): d['id'] = self.id
        if self.not_empty(self.artist): d['artist'] = self.artist
        if self.not_empty(self.title): d['title'] = self.title
        if self.not_empty(self.description): d['description'] = self.description
        if self.not_empty(self.picture): d['picture'] = self.picture
        if self.not_empty(self.thumbnail): d['thumbnail'] = self.thumbnail
        if self.not_empty(self.ebay): d['ebay'] = self.ebay
        if self.not_empty(self.venue): d['venue'] = self.venue
        if self.not_empty(self.medium): d['medium'] = self.medium
        d['sold'] = self.sold
        return str(d)
