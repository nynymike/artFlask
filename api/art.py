"""
.. currentmodule:: api.art

Art API
-------

.. http:get:: /art/(art_id)
.. http:get:: /art/(art_id)/(action)

   Returns the Art entity for the given art_id. If the action is ``picture`` , ``thumbnail``,
   ``qrcode``, ``view``

   **Example request**:

   .. sourcecode:: http

      GET /art/68b4f17f-bd76-4338-a59f-15b4a097a31b HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   :statuscode 200: no error
   :statuscode 404: no such art

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

def getArt(art_id):
    return {}

def getThumbnail(art_id):
    return ""

def getPicture(art_id):
    return ""

class Art(Resource):
    def get(self, art_id=None, action_type=None):
        if not art_id: return 'Art not found', 404
        else:
            if action_type=="thumbnail":
                return getThumbnail(art_id)
            if action_type=="picture":
                return getPicture(art_id)
            return getArt(art_id)