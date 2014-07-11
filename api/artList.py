from flask import request, abort
from flask.ext.restful import Resource, reqparse
from flask.json import jsonify
from sqlalchemy.exc import IntegrityError

from utils.app_ctx import ApplicationContext
from app import db
# from flask_restful.utils import cors

from model import Artwork, Website


def website_list_from_dict(website_dict):
    return [Website(name=name, url=url) for name, url in website_dict.items()]


def art_list_from_ids(ids):
    return Artwork.query.filter(Artwork.id.in_(ids)).all()


class ArtList(Resource):
    REQUIRED = ['title', 'description', 'buy_url', 'venue', 'medium', 'sold']

    # @cors.crossdomain(origin='*')
    def get(self):
        app_ctx = ApplicationContext('Artwork')
        items = app_ctx.query_from_context(allowList=False)
        # from utils.helpers import JsonModelEncoder
        # return json.dumps(items.all(), cls=JsonModelEncoder)
        return jsonify(item_list=[item.as_dict() for item in items])

    # @cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        for field in Artwork.__table__.columns:
            required = (field.name in self.REQUIRED)
            if field.name == 'venue_id':
                input_name = 'venue'
            elif field.name == 'artist_id':
                input_name = 'artist'
            elif field.name == 'parent_id':
                input_name = 'parent_work'
            else:
                input_name = field.name

            parser.add_argument(input_name, type=field.type.python_type,
                                dest=field.name, required=required)
        parser.add_argument('alt_urls', type=website_list_from_dict, required=False)
        parser.add_argument('series', type=art_list_from_ids, required=False)

        args = {k: v for k, v in parser.parse_args(request).items() if v}
        try:
            item = Artwork(**args)
            db.session.add(item)
            db.session.commit()

            return "%d" % item.id, 201
        except IntegrityError:
            abort(403)



