"""
.. currentmodule:: api.manage

Manage API
----------

   Functionality available to the tour admin. Access to ``/manage`` APIs are restricted
   to people with the ``staff`` value for user claim ``role``.

.. http:post:: /manage/event

   Add a new event and return newly created event id. See JSON schema for data format.
   No need to post event id--it will be automatically generated.

   :statuscode 201: Event Created
   :statuscode 404: Error creating event

.. http:put:: /manage/event/(event_id)

    Update an event by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Event not found

.. http:post:: /manage/venue

   Add a new venue and return newly created venue id. See JSON schema for data format.
   No need to post venue id--it will be automatically generated.

   :statuscode 201: Venue Created
   :statuscode 404: Error creating Venue

.. http:put:: /manage/venue/(venue_id)

    Update an venue by sending new JSON. See JSON schema for data format.

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

