"""
.. currentmodule:: api.staff

Staff API
---------

   Staff listing and detail

.. http:get:: /staff
.. http:get:: /staff/(staff_id)

   :statuscode 200: no error
   :statuscode 404: staff member not found

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api


class Staff(Resource):
    def getAllStaff(self):
        return []
    def getStaff(self, staff_id):
        return {}
    def get(self, staff_id=None):
        if not staff_id: return 'Event not found', 404
        return self.getStaff(staff_id)

