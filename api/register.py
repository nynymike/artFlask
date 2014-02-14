"""
.. currentmodule:: api.register

Register API
------------

   Registration workflow

.. http:post:: /register

   Send a Person entity to request registration. The following fields may be 
   posted for registration : name, given_name, family_name, middle_name,
   nickname, picture, website, email, gender, birthdate, phone_number, address,
   twitter, social_urls, preferred_contact

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



