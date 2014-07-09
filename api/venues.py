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

import json

from flask.ext.restful import Resource, Api
from flask import Request
from flask_restful.utils import cors

from utils.helpers import jsonify
from utils.app_ctx import ApplicationContext
from bson import json_util


class Venues(Resource):
    #@cors.crossdomain(origin='*')
    def get(self, venue_id):
        app_ctx = ApplicationContext('Venue')
        item = app_ctx.get_item(venue_id)
        if not item:
            return {}, 404
        return item


class VenueList(Resource):
    #@cors.crossdomain(origin='*')
    def get(self):
        app_ctx = ApplicationContext('Venue')
        venues = app_ctx.query_from_context(allowList=True)

        return jsonify(item_list=[item.as_dict() for item in venues])

