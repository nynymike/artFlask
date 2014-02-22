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
from utils.helpers import jsonify
from utils.app_ctx import ApplicationContext
import json
from bson import json_util

def getVenue(venue_id):
    return {}

def queryVenues(query):
    return {}

class Venues(Resource):
    def get(self,venue_id):
      app_ctx =ApplicationContext('venue')
      try:
        item = app_ctx.get_item(venue_id)
        return json_util.dumps(item)
      except Exception , e:
        return str(e), 404

class VenueList(Resource):
      def get(self):
        app_ctx =ApplicationContext('venue')
        try:
          venue = app_ctx.query_from_context(allowList=True)
          return json_util.dumps(venue)
        except:
          return 'venue not found', 404

