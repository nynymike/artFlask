from flask.ext.restful import Resource, Api
from flask_restful_swagger import swagger
from flask_restful.utils import cors

from utils.helpers import upload_file, jsonify
from utils.app_ctx import ApplicationContext
from model import Person


class ArtistList(Resource):
    MODEL = Person

    # @cors.crossdomain(origin='*')
    @swagger.operation(
        summary='get artists list',
        responseClass=MODEL.__name__,
        nickname='getArtists',
        parameters=[],
    )
    def get(self):
        app_ctx = ApplicationContext('Person')
        items = app_ctx.query_from_context(allowList=True, default_data={'role': 'artist'})
        return jsonify(item_list=[item.as_dict() for item in items])
