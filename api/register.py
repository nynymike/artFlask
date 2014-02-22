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
from bson.objectid import ObjectId
from utils.app_ctx import ApplicationContext
from db import mongo
from flask.ext.mail import Message
from flask import current_app
from mail import mail
class Register(Resource):

    def post(self):
      #args = self.parser.parse_args()
      #return None,200
      try:
        required_fields = ['email',
                          'given_name',
                          'family_name',
                          'phone_number',
                          'sub']
        unique_fields = ['email']
        app_ctx = ApplicationContext('person')
        code = "%s"%ObjectId()
        registration_id = app_ctx.create_item_from_context(required_fields=required_fields,unique_fields=unique_fields)
        data = {'status':'Pending',
                'registration_code':{'code':code, 'sent': datetime.datetime.now(),
                         'accepted': None}
                }
        mongo.db.Person.update({'_id': ObjectId(registration_id)},{"$set": data},upsert=False)
        user = mongo.db.Person.find({'_id': ObjectId(registration_id)}).next()
        url = current_app.config['BASE_URL']+ "api/v1/register/%s"%code
        html = "Please click <a href='%s'>here</a> to verify your email address or copy paste %s in browser"% (url,url)
        message = Message(subject='Verify your email address', html=html, recipients=[user['email']],sender=current_app.config['DEFAULT_MAIL_SENDER'])
        mail.send(message)
        return '',200
      except Exception, e:
        return str(e),404

    def get(self,token):
        try:
          user = mongo.db.Person.find({'registration_code.code':token}).next()
          mongo.db.Person.update({'_id': ObjectId("%s"%user['_id'])},{"$set": {'status':'Active'}},upsert=False)
          return '',200
        except Exception, e:
          print str(e)
          return 'user not found',404




