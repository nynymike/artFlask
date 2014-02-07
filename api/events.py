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

def getEvent(event_id):
    return [{}]

def getAllEvents():
    return []

class Events(Resource):
    def get(self, event_id=None):
        if not event_id:
            return getAllEvents()
        else:
            return getEvent(event_id)