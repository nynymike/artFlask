"""
.. currentmodule:: api.art

Art API
-------
.. http:get:: /art

   Search art. Returns a list of Art entities.

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /art/(art_id)
.. http:get:: /art/(art_id)/(action)

   Returns the Art entity for the given art_id. If the action is ``picture`` , ``thumbnail``,
   ``qrcode``, return image from filesystem. If ``view`` return artView.html template

   **Example request**:

   .. sourcecode:: http

      GET /art/68b4f17f-bd76-4338-a59f-15b4a097a31b HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: no such art

.. http:post:: /art

   Uploads a new file, returning the newly created art id. At this time, the thumbnail,
   watermarked web sized image, and QR code for the view should be generated. For now,
   these will be stored in the ``upload`` folder and given filenames of
   <id>-web.png, <id>-tn.png, and <id>-qr.png where <id> is the Art ID field.
   Note image funtions are in api/artImageFunctions.py (see test() method).
   Original uploaded binary will be deleted.

   :form file: File to be uploaded
   :form title: Title of the work
   :form description: Description of the work
   :form buyURL: E-commerce website to buy work
   :form venue: Venue ID
   :form medium: Artwork materials and style
   :form sold: Whether the work is sold
   :form series: List of Art IDs for related works
   :form parent_work: Art ID of work that is the parent, or provides some other context
   :form alt_urls: List of alternate URLs to display.

   :statuscode 201: Art Created
   :statuscode 404: Error uploading

.. http:put:: /art/(art_id)

   Update artwork by sending a json object for a given work. Note, if a new image is
   uploaded, you must re-generate the -web and -tn images using artImageFunctions.py

   :jsonparam string file: base64 encoded bytes for the image
   :jsonparam string title: Title of the work
   :jsonparam string description: Description of the work
   :jsonparam string buyURL: Ecommerce website to buy work
   :jsonparam string venue: Venue ID
   :jsonparam string medium: Artwork materials and style
   :jsonparam boolean sold: Whether the work is sold
   :jsonparam series: List of Art IDs for related works
   :jsonparam parent_work: Art ID of work that is the parent, or provides some other context
   :jsonparam alt_urls: List of alternate URLs to display.

   :statuscode 200: Update Successful
   :statuscode 404: Error uploading

.. http:delete:: /art/(art_id)

   Delete an artwork (must be owned by the person).

   :statuscode 200: Delete Successful
   :statuscode 404: Not found

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

    def delete(self):
        # Find item
        # Check authorizatoin
        # Delete file
        if False: return '',404
        return '',200
