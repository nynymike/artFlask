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

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: no such art

.. http:post:: /art

   Uploads a new file, returning the newly created art id

   :form file: File to be uploaded
   :form title: Title of the work
   :form description: Description of the work
   :form ebay: Ebay URL
   :form venue: Venue ID
   :form medium: Artwork materials and style
   :form sold: Whether the work is sold

   :statuscode 201: Art Created
   :statuscode 404: Error uploading

.. http:put:: /art/(art_id)

   Update artwork by sending a json object for a given work.

   :jsonparam string file: base64 encoded bytes for the image
   :jsonparam string title: Title of the work
   :jsonparam string description: Description of the work
   :jsonparam string ebay: Ebay URL
   :jsonparam string venue: Venue ID
   :jsonparam string medium: Artwork materials and style
   :jsonparam boolean sold: Whether the work is sold

   :statuscode 200: Update Successful
   :statuscode 404: Error uploading

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api
from flask import Request

def getArt(art_id):
    return {}

def getThumbnail(art_id):
    return ""

def getPicture(art_id):
    return ""

class Art(Resource):
    def get(self, art_id=None, action_type=None):
        if not art_id:
            query = Request.args
            if not len(query):
                return 'Art not found', 404
            else:
                return queryArt(query)
        else:
            if action_type=="thumbnail":
                return getThumbnail(art_id)
            if action_type=="picture":
                return getPicture(art_id)
            return getArt(art_id)

    def post(self):
        # Get params and write
        # Convert image to web size
        # Write file
        # Convert image to thumbnail
        # Write file
        # Create db entry for art
        if False: return '',404
        return '',201

    def put(self):
        # Get file from json data and base64 decode
        # Convert image to web size
        # Write file
        # Convert image to thumbnail
        # Update db entry for art
        if False: return '',404
        return '',200

