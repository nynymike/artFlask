"""
.. currentmodule:: api.artists


Artists API
-----------

.. http:get:: /artists

   Search artists. Returns a list of Person entities.

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: nothing found

.. http:get:: /artists/(artist_id)

   Returns a JSON Person entity for the specified artist

   :query [see schema]: substring for which to search

   :statuscode 200: no error
   :statuscode 404: no such artist

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, marshal_with
from flask_restful_swagger import swagger
from bson import json_util
import json

from utils.app_ctx import ApplicationContext
from model import Person


def getAllArtists():
    return []


def getArtist(personID):
    return {}


def queryResults(query):
    return {}


class Artists(Resource):
    """
    Artists API
    """
    MODEL = Person

    @swagger.operation(
        notes='get a single artist',
        responseClass=MODEL.__name__,
        nickname='get',
        parameters=[
            {
                'name': 'artist_id',
                'dataType': 'string',
                'description': 'openid identifier',
                'required': True,
            }
        ]
    )
    # @marshal_with(resource_fields)
    def get(self, artist_id):
        app_ctx = ApplicationContext('Person')
        try:
            item = app_ctx.get_item(artist_id)
            return json.loads(json_util.dumps(item))
        except Exception as e:
            return str(e), 404

