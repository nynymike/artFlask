"""
.. currentmodule:: model.Event

Event Entity Schema
-------------------

+------------+-------------------+------------------------------------------------------------------------+
| member     | type              | description                                                            |
+============+===================+========================================================================+
| id         | string            | unique identifier for the event                                        |
+------------+-------------------+------------------------------------------------------------------------+
| startDate  | string            | Date the event starts                                                  |
+------------+-------------------+------------------------------------------------------------------------+
| endDate    | string            | Date the event ends                                                    |
+------------+-------------------+------------------------------------------------------------------------+
| name       | string            | name of the event                                                      |
+------------+-------------------+------------------------------------------------------------------------+
| picture    | string            | URI for a tiny jpg or png event logo                                   |
+------------+-------------------+------------------------------------------------------------------------+
| venues     | List <string>     | List venue ids                                                         |
+------------+-------------------+------------------------------------------------------------------------+

Event Entity JSON sample:
-------------------------

.. code-block:: javascript

        {
        'id': 'd0291047-aded-41f1-8ef6-3fc76700e58b',
        'startDate': 'Feb  3 00:00:00 UTC 2014',
        'endDate': 'Feb  5 00:00:00 UTC 2014',
        'name': 'Happy Tour 2014',
        'picture': 'http://tour.org/logo/happy2014.png',
        'venues': ['6b5ce4a8-6141-442b-8846-9adf34c5c7a7', '4e8590f3-cfb0-4cec-869b-0f9b3f70c81f']
        }

"""

class ArtWork():
    def __init__(self):
        self.id = ""
        self.artist = ""
        self.title = ""
        self.picture = ""
        self.thumbnail = ""
        self.ebay = ""
        self.venue = ""

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        if self.not_empty(self.id): d['id'] = self.id,
        if self.not_empty(self.artist): d['artist'] = self.artist,
        if self.not_empty(self.title): d['title'] = self.title,
        if self.not_empty(self.picture): d['picture'] = self.picture,
        if self.not_empty(self.thumbnail): d['thumbnail'] = self.thumbnail,
        if self.not_empty(self.ebay): d['ebay'] = self.ebay,
        if self.not_empty(self.venue): d['venue'] = self.venue
        return str(d)
