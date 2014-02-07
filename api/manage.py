"""
.. currentmodule:: api.manage

Manage API
----------

   Functionality available to the tour admin. Access to ``/manage`` APIs are restricted
   to people with the ``staff`` value for user claim ``role``.

.. http:put:: /manage/event/(event_id)

    Update an event by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Event not found

.. http:post:: /manage/event

   Add a new event and return newly created event id. Returns new event id.

   :statuscode 201: Event Created
   :statuscode 404: Error creating event

.. http:delete:: /manage/event/(event_id)

   Delete an event.

   :statuscode 200: Event Deleted
   :statuscode 404: Not found

.. http:put:: /manage/venue/(venue_id)

    Update an venue by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Venue not found

.. http:post:: /manage/venue

   Add a new venue and return newly created venue id. See JSON schema for data format.
   No need to post venue id--it will be automatically generated.

   :statuscode 201: Venue Created
   :statuscode 404: Error creating Venue

.. http:delete:: /manage/venue/(venue_id)

    Delete a venue.

   :statuscode 200: no error
   :statuscode 404: Venue not found

.. http:post:: /manage/person

   Add a new person and return newly created person id. See JSON schema for data format.
   No need to post person id--it will be automatically generated.

   :statuscode 201: Person Created
   :statuscode 404: Error creating Person

.. http:put:: /manage/person/(person_id)

    Update an person by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Person not found

.. http:delete:: /manage/person/(person_id)

    Deletes person

   :statuscode 200: no error
   :statuscode 404: Person not found

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
