"""
.. currentmodule:: api.profile

Profile API
-----------

   Enables a person to view and update their profile in the tour.

.. http:get:: /profile

    Return Person Entity for person currently logged in.

   :statuscode 200: no error
   :statuscode 404: Event not found

.. http:put:: /profile

   Send a Person Entity to update profile of currently logged in person.
   Some attributes may not be writable. todo: list attributes

   :statuscode 200: Update Successful
   :statuscode 404: Error updating

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

class ManageEvent(Resource):
    def put(self, event_id=None):
        if not event_id: return 'Event not found', 404
        else:
            return None
    def post(self, event_id=None):
        if not event_id: return 'Event not found', 404
        else:
            return None
    def delete(self, event_id=None):
        if not event_id: return 'Event not found', 404
        else:
            return None

class ManageVenue(Resource):
    def put(self, venue_id=None):
        if not venue_id: return 'Venue not found', 404
        else:
            return None

    def post(self, venue_id=None):
        if not venue_id: return 'Venue not found', 404
        else:
            return None

    def delete(self, venue_id=None):
        if not venue_id: return 'Venue not found', 404
        else:
            return None

class ManagePerson(Resource):
    def put(self, person_id=None):
        if not person_id: return 'Person not found', 404
        else:
            return None
    def post(self, person_id=None):
        if not person_id: return 'Person not found', 404
        else:
            return None
    def delete(self, person_id=None):
        if not person_id: return 'Person not found', 404
        else:
            return None
