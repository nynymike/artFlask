from flask import  request 
from flask.ext.restful import Resource, Api
from utils.helpers import  upload_file, jsonify
from utils.app_ctx import ApplicationContext
from bson import json_util


class ArtistList(Resource):

    def get(self):
      app_ctx =ApplicationContext('person')
      items = app_ctx.query_from_context(allowList=True)
      return json_util.dumps(items)