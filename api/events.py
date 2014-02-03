"""
.. currentmodule:: api.events

Events API
----------

.. http:get:: /event/(event_name)

   Returns the respective Event entity

   :statuscode 200: no error
   :statuscode 404: no such event
   :statuscode 422: duplicate event - contact staff

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

def getEvent(event_id):
    return [{}]

class Events(Resource):
    def get(self, event_id=None):
        if not event_id: return 'Event not found', 404
        else:
            event = getEvent(event_id)
            if len(getEvent) > 1: 'duplicate event - contact staff', 422
            return getEvent(event_id)