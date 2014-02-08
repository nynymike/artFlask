"""
.. currentmodule:: api.register

Register API
------------

   Registration workflow

.. http:get:: /register/(registration_id)

   Validates the person's registration and asks them to choose a password.
   Sends a SCIM update to oxTrust to add the person for OpenID Connect
   authentication.

.. http:post:: /register

   Send a Person entity to request registration.

   :statuscode 200: Registration request successful
   :statuscode 406: Duplicate registration

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

class Register(Resource):
    def get(self, registration_id=None):
        return {}

    def put(self, person=None):
        return None


