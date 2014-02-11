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

class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('given_name', type=str)
        self.parser.add_argument('family_name', type=str)
        self.parser.add_argument('middle_name', type=str)
        self.parser.add_argument('nickname', type=str)
        self.parser.add_argument('picture', type=str)
        self.parser.add_argument('website', type=str)
        self.parser.add_argument('email', type=str)
        self.parser.add_argument('gender', type=str)
        self.parser.add_argument('birthdate', type=str)
        self.parser.add_argument('phone_number', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('twitter', type=str)
        self.parser.add_argument('preferred_contact', type=str)
        self.parser.add_argument('social_urls', type=str)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['artFlask']
        self.collection = db['people']

    def __del__(self):
        self.client.disconnect()

    def post(self):
        args = self.parser.parse_args()

        return None,200

    def get(self, registration_id=None):
        return {}



