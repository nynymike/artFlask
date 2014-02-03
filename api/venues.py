"""
.. currentmodule:: api.venues

Venues API
----------

.. http:get:: /venues/(venue_id)

   Returns the Venue entity for the given venue_id.

   :statuscode 200: no error
   :statuscode 404: no such venue

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

def getVenue(venue_id):
    return {}

class Venues(Resource):
    def get(self, venue_id=None):
        if not venue_id: return 'Venue not found', 404
        else:
            return getVenue(venue_id)