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


from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from utils.helpers import jsonify
from utils.app_ctx import ApplicationContext

from model import Venue


class Venues(Resource):
    """
    API to handle single venues
    """
    MODEL = Venue

    @swagger.operation(
        summary='get a single event object',
        responseClass=MODEL.__name__,
        nickname='getVenue',
        parameters=[
            {
                'name': 'venue_id',
                'dataType': 'integer',
                'description': 'identifier of a venue object',
                'required': True,
            }
        ]
    )
    def get(self, venue_id):
        app_ctx = ApplicationContext('Venue')
        item = app_ctx.get_item(venue_id)
        if not item:
            return {}, 404
        return item


class VenueList(Resource):
    """
    Bulk venues API.
    """
    MODEL = Venue

    @swagger.operation(
        summary='get a list of all venues',
        responseClass=MODEL.__name__,
        nickname='getVenueList',
        parameters=[]
    )
    def get(self):
        app_ctx = ApplicationContext('Venue')
        venues = app_ctx.query_from_context(allowList=True)

        return jsonify(item_list=[item.as_dict() for item in venues])

