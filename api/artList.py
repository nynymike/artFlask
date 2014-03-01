from flask import  request 
from flask.ext.restful import Resource, Api
from utils.helpers import  upload_file, jsonify
from utils.app_ctx import ApplicationContext
from bson import json_util
import json

class ArtList(Resource):

    def get(self):
      app_ctx =ApplicationContext('art')
      items = app_ctx.query_from_context(allowList=False)
      return json.loads(json_util.dumps(items))
    def post(self):
        # Get params and write
        # Convert image to web size
        # Write file
        # Convert image to thumbnail
        # Write file
        # Create db entry for art
        # try:
          app_ctx = ApplicationContext('art')
          # if 'file' in request.files:
          #   upload_file()
          item_id = app_ctx.create_item_from_context()
          return "%s"%item_id,201
        # except Exception, e:
        #   return str(e),404