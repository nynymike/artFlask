"""
.. currentmodule:: api.staff

Staff API
---------

   Entity write operations. Access to staff APIs is restricted to people with the ``staff`` valie
   for user claim ``role``.

.. http:get:: /staff/event/(event_id)
.. http:get:: /staff/venue/(venue_id)
.. http:get:: /staff/person/(person_id)

   :statuscode 200: no error
   :statuscode 404: no error

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

class ManageEvent(Resource):
    def get(self, event_id=None):
        if not event_id: return 'Event not found', 404
        else:
            return None

class ManageVenue(Resource):
    def get(self, venue_id=None):
        if not venue_id: return 'Venue not found', 404
        else:
            return None

class ManagePerson(Resource):
    def get(self, person_id=None):
        if not person_id: return 'Person not found', 404
        else:
            return None