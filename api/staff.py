"""
.. currentmodule:: api.staff

Staff API
---------

   Staff listing and detail

.. http:get:: /staff

   List all staff, or search staff

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /staff/(staff_id)

   :statuscode 200: no error
   :statuscode 404: staff member not found

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api
from utils.app_ctx import ApplicationContext
import json
from bson import json_util
from flask_restful.utils import cors

class Staff(Resource):
    #@cors.crossdomain(origin='*')
    def get(self,person_id):
        app_ctx =ApplicationContext('Person')
        try:
            item = app_ctx.get_item(person_id)
            return json.loads(json_util.dumps(item))
        except Exception , e:
            return str(e), 404

class StaffList(Resource):
    #@cors.crossdomain(origin='*')
    def get(self):
        app_ctx =ApplicationContext('Person')
        try:
          staff = app_ctx.query_from_context(allowList=True,default_data={'role':'staff'})
          return json.loads(json_util.dumps(staff))
        except:
          return 'venue not found', 404

