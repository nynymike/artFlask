"""
.. currentmodule:: api.profile

Profile API
-----------

   Enables a person to view and update their profile in the tour.

.. http:get:: /profile

    Return Person entity for person currently logged in.

   :statuscode 200: no error
   :statuscode 404: Event not found

.. http:put:: /profile

   Send a Person entity to update profile of currently logged in person.
   Some attributes may not be writable. todo: list attributes

   :statuscode 200: Update Successful
   :statuscode 404: Error updating

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

class Profile(Resource):
    def get(self):
        return {}

    def put(self, person=None):
        return None


