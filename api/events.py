"""
.. currentmodule:: api.events

Events API
----------

.. http:get:: /events/

   Search events. Returns a list of Event entities.

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /events/(event_name)

   Returns Event entity

   :statuscode 200: no error
   :statuscode 404: no such event

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from utils.helpers import jsonify
from utils.app_ctx import ApplicationContext
from model import Event


class Events(Resource):
    """
    API to handle single events
    """

    MODEL = Event

    @swagger.operation(
        summary='get a single event object',
        responseClass=MODEL.__name__,
        nickname='getEvent',
        parameters=[
            {
                'name': 'event_id',
                'dataType': 'integer',
                'description': 'identifier of an event object',
                'required': True,
            }
        ]
    )
    def get(self, event_id):
        app_ctx = ApplicationContext('Event')
        item = app_ctx.get_item(event_id)
        if not item:
            return {}, 404
        return item


class EventList(Resource):
    """
    Bulk events API.
    """

    MODEL = Event

    @swagger.operation(
        summary='get a list of all events',
        responseClass=MODEL.__name__,
        nickname='getEventList',
        parameters=[]
    )
    def get(self):
        app_ctx = ApplicationContext('Event')
        events = app_ctx.query_from_context(allowList=True)
        return jsonify(item_list=[item.as_dict() for item in events])
