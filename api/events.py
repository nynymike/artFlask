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

def getEvent(event_id):
    return [{}]

def getAllEvents():
    return []

class Events(Resource):
    def get(self, event_id=None):
      app_ctx =ApplicationContext('event')
      # try:
      events = app_ctx.query_from_context(allowList=True)
      return json_util.dumps(events)
      # except:
      #     return 'Event not found', 404
