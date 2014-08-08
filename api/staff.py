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

import json

from flask.ext.restful import Resource, Api, abort
from flask_restful.utils import cors
from bson import json_util

from utils.app_ctx import ApplicationContext
from utils.helpers import jsonify
from model import Person


class Staff(Resource):
    #@cors.crossdomain(origin='*')
    def get(self, person_id):
        p = Person.query.get(person_id)
        if not p:
            abort(404)
        return p.as_dict()


class StaffList(Resource):
    #@cors.crossdomain(origin='*')
    def get(self):
        staff = Person.query.filter_by(role='staff')
        if len(staff) == 0:
            abort(404)
        return jsonify(item_list=[s.as_dict() for s in staff])
