"""
.. currentmodule:: api.art

Art API
-------
.. http:get:: /art

   Search art: returns a list of Art entities. GET requests to this URL without query
   parameters will return 501 (Not Implemented), as requests to dump all the Art data
   is discouraged.

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

import json

from flask import request, abort
from flask.ext.restful import Resource, reqparse
from flask_restful.utils import cors
from flask_restful_swagger import swagger

from utils.helpers import upload_file
from utils.app_ctx import ApplicationContext
from bson import json_util

from model import Artwork, Person, Website
from app import db


# FIXME(analytic): copy-paste from artlist.py
def website_list_from_dict(website_dict):
    return [Website(name=name, url=url) for name, url in website_dict.items()]


def art_list_from_ids(ids):
    return Artwork.query.filter(Artwork.id.in_(ids)).all()


class Art(Resource):
    """Art resource"""
    MODEL = Artwork

    @swagger.operation(
        method='GET',
        summary='get a single art object',
        responseClass=MODEL.__name__,
        nickname='getArtwork',
        parameters=[
            {
                'name': 'art_id',
                'dataType': 'integer',
                'description': 'identifier of an art object',
                'required': True,
            }
        ]
    )
    def get(self, art_id):
        app_ctx = ApplicationContext('Art')
        item = app_ctx.get_item(art_id)
        if not item:
            return {}, 404
        return item

    @swagger.operation(
        method='PUT',
        summary="update a single art object",
        responseClass=MODEL.__name__,
        nickname='updateArtwork',
        parameters=[
            {
                'name': 'art_id',
                'dataType': 'integer',
                'description': 'identifier of an art object',
                'required': True,
            }
        ]
    )
    def put(self, art_id=None):
        artwork = self.MODEL.query.get(art_id)
        if not artwork:
            abort(404)

        parser = reqparse.RequestParser()
        for field in Artwork.__table__.columns:
            if field.name == 'venue_id':
                input_name = 'venue'
            elif field.name == 'artist_id':
                input_name = 'artist'
            elif field.name == 'parent_id':
                input_name = 'parent_work'
            else:
                input_name = field.name

            parser.add_argument(input_name, type=field.type.python_type,
                                dest=field.name)

        parser.add_argument('alt_urls', type=website_list_from_dict)
        parser.add_argument('series', type=art_list_from_ids)

        for k, v in parser.parse_args(request).items():
            if v is not None:
                setattr(artwork, k, v)
        db.session.commit()

    @swagger.operation(
        method='DELETE',
        summary="delete a single art object",
        responseClass=MODEL.__name__,
        nickname='delete',
        parameters=[
            {
                'name': 'art_id',
                'dataType': 'integer',
                'description': 'identifier of an art object',
                'required': True,
            }
        ]
    )
    def delete(self, art_id=None):
        o = self.MODEL.query.get(art_id)
        if not o:
            abort(404)
        db.session.delete(o)
        db.session.commit()

