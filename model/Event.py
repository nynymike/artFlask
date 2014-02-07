"""
.. currentmodule:: model.Event

Event Entity Schema
-------------------

+-------------+-------------------+------------------------------------------------------------------------+
| member      | type              | description                                                            |
+=============+===================+========================================================================+
| id          | string            | unique identifier for the event                                        |
+-------------+-------------------+------------------------------------------------------------------------+
| name        | string            | Name of the event - must be unique                                     |
+-------------+-------------------+------------------------------------------------------------------------+
| startDate   | string            | Date the event starts                                                  |
+-------------+-------------------+------------------------------------------------------------------------+
| endDate     | string            | Date the event ends                                                    |
+-------------+-------------------+------------------------------------------------------------------------+
| description | string            | Text descrition of the event                                           |
+-------------+-------------------+------------------------------------------------------------------------+
| picture     | string            | URI for a tiny jpg or png event logo                                   |
+-------------+-------------------+------------------------------------------------------------------------+

Event Entity JSON sample:
-------------------------

.. code-block:: javascript

        {
        'id': 'happy2014',
        'name': 'Happy Tour 2014',
        'startDate': 'Feb  3 00:00:00 UTC 2014',
        'endDate': 'Feb  5 00:00:00 UTC 2014',
        'description': 'This is a tour of all the artwork that you would want to see to make you smile',
        'picture': 'http://happytour.org/happy2014.png'
        }

"""

class Event():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.startDate = ""
        self.endDate = ""
        self.description = ""
        self.picture = ""

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        if self.not_empty(self.id): d['id'] = self.id,
        if self.not_empty(self.name): d['name'] = self.name,
        if self.not_empty(self.startDate): d['startDate'] = self.startDate,
        if self.not_empty(self.endDate): d['endDate'] = self.endDate,
        if self.not_empty(self.description): d['description'] = self.description,
        if self.not_empty(self.picture): d['picture'] = self.picture

    return str(d)
