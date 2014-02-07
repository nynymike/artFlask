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

def getAllArtists():
    return []

def getArtist(personID):
    return {}

def queryResults(query):
    return {}

class Artists(Resource):
    def get(self, person_id=None, action_id=None):
        if not person_id:
            query = Request.args
            if not len(query):
                return getAllArtists()
            else:
                return queryResults(query)
        else: return getArtist(person_id)

