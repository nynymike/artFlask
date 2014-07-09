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

from flask.ext.restful import Resource, Api
from utils.helpers import jsonify, request_to_dictonary
from utils.app_ctx import ApplicationContext
import json
from bson import json_util
from flask_restful.utils import cors


class Event(Resource):
    #@cors.crossdomain(origin='*')
    def get(self, event_id):
        app_ctx = ApplicationContext('Event')
        item = app_ctx.get_item(event_id)
        if not item:
            return {}, 404
        return item


class EventList(Resource):
    #@cors.crossdomain(origin='*')
    def get(self, event_id=None):
        app_ctx = ApplicationContext('Event')
        events = app_ctx.query_from_context(allowList=True)
        return jsonify(item_list=[item.as_dict() for item in events])
