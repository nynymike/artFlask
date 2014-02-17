"""
.. currentmodule:: api.register

Register API
------------

   Registration workflow

.. http:post:: /register

   Send a Person entity to request registration. Check the Person Entity for
   required fields. A registration_code is generated and stored in the Person
   entity. The Person's status entry will be 'Pending' until the activation
   link is clicked.

   On registration, the person will be sent and email with
   an activation link.

   :statuscode 200: Registration request successful
   :statuscode 406: Duplicate registration

.. http:get:: /register/(registration_id)

   Validates the person's registration and asks them to choose a password.
   Sends a SCIM update to oxTrust to add the person for OpenID Connect
   authentication.

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api, reqparse
from pymongo import MongoClient
import datetime
from utils.app_ctx import ApplicationContext

class Register(Resource):

    def post(self):
      #args = self.parser.parse_args()
      #return None,200
      try:
        app_ctx = ApplicationContext('person')
        app_ctx.create_item_from_context()
        return '',200
      except Exception, e:
        return '',406

    def get(self, registration_id=None):
        return {}



