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

from flask.ext.restful import Resource, Api
from flask import Request
from flask.ext.restful import reqparse
from utils.app_ctx import ApplicationContext
from bson import json_util
import json
from flask_restful.utils import cors


def getAllArtists():
    return []


def getArtist(personID):
    return {}


def queryResults(query):
    return {}


class Artists(Resource):

    #@cors.crossdomain(origin='*')
    def get(self, artist_id):
        app_ctx = ApplicationContext('person')
        try:
            item = app_ctx.get_item(artist_id)
            return json.loads(json_util.dumps(item))
        except Exception as e:
            return str(e), 404

