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
from utils.helpers import jsonify
from utils.app_ctx import ApplicationContext

class Profile(Resource):
    def get(self):
      app_ctx =ApplicationContext('person')
      try:
        item = app_ctx.get_item(event_id)
        return jsonify(item)
      except:
        return 'Event not found', 404

    def put(self, person=None):
        return None


