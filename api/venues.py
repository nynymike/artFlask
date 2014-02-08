"""
.. currentmodule:: api.venues

Venues API
----------

.. http:get:: /venues
    Search venues. Returns a list of Venue entities

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /venues/(venue_id)

   Returns the Venue entity for the given venue_id.

   :statuscode 200: no error
   :statuscode 404: no such venue

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api
from flask import Request

def getVenue(venue_id):
    return {}

def queryVenues(query):
    return {}

class Venues(Resource):
    def get(self, venue_id=None):
        if not venue_id:
            query = Request.args
            if not len(query):
                return 'Venue or query not found', 404
            else:
                return queryVenues(query)
        else:
            return getVenue(venue_id)