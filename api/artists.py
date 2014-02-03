"""
.. currentmodule:: api.artists


Artists API
-----------

.. http:get:: /artists/(artist_id)

   Returns a JSON Person entity for the specified artist

   :statuscode 200: no error
   :statuscode 404: no such artist

"""
__author__ = 'Michael Schwartz'

from flask.ext.restful import Resource, Api

def getAllArtists():
    return []

def getArtist(personID):
    return {}

class Artists(Resource):
    def get(self, person_id=None, action_id=None):
        if not person_id : return getAllArtists()
        else: return getArtist(person_id)