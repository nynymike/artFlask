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
from flask_restful.utils import cors


# class Profile(Resource):
    #@cors.crossdomain(origin='*')
    # def get(self):
    #   app_ctx =ApplicationContext('Person')
    #   try:
    #     item = app_ctx.get_item(event_id)
    #     return jsonify(item)
    #   except:
    #     return 'Person not found', 404
    #
    # #@cors.crossdomain(origin='*')
    # def put(self, person=None):
    #     return None


