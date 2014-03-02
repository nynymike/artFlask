from flask import  request 
from flask.ext.restful import Resource, Api
from flask_restful.utils import cors
from utils.helpers import  upload_file, jsonify
from utils.app_ctx import ApplicationContext
from bson import json_util
import json

class ArtistList(Resource):
    @cors.crossdomain(origin='*')
    def get(self):
        app_ctx =ApplicationContext('person')
        items = app_ctx.query_from_context(allowList=True,default_data={'role':'artist'})
        return json.loads(json_util.dumps(items))