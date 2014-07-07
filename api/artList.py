from flask.ext.restful import Resource
from flask.json import jsonify
from utils.app_ctx import ApplicationContext
# from flask_restful.utils import cors


class ArtList(Resource):
    # @cors.crossdomain(origin='*')
    def get(self):
        app_ctx = ApplicationContext('Artwork')
        items = app_ctx.query_from_context(allowList=False)
        # from utils.helpers import JsonModelEncoder
        # return json.dumps(items.all(), cls=JsonModelEncoder)
        return jsonify(item_list=[item.as_dict() for item in items])

    # @cors.crossdomain(origin='*')
    def post(self):
        # Get params and write
        # Convert image to web size
        # Write file
        # Convert image to thumbnail
        # Write file
        # Create db entry for art
        # try:
        app_ctx = ApplicationContext('Artwork')
        # if 'file' in request.files:
        #   upload_file()
        item = app_ctx.create_item_from_context()
        return "%d" % item.id, 201
        # except Exception, e:
        #   return str(e),404