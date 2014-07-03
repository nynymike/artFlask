import json
import datetime

from flask import request
from flask.ext.restful import reqparse

# from db import mongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from werkzeug import Response

from api.artImageFunctions import *


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def request_to_dictonary(model_class, typeSafe=True):
    parser = reqparse.RequestParser()
    for field in model_class.__table__.columns:
        if typeSafe:
            parser.add_argument(field.name, type=field.type.python_type)
        else:
            parser.add_argument(field.name)
    args = {k: v for k, v in parser.parse_args(request).items() if v}
    return args


# def update_from_dictionary(data, item, model_class, object_id=None):
#     if object_id is None:
#         return getattr(mongo.db, model_class._collection_).save(data)
#     else:
#         return getattr(mongo.db, model_class._collection_).update(
#             {'_id': ObjectId(object_id)},
#             {"$set": data},
#             upsert=False)


# def remove_record_by_id(object_id,model_class):
#     getattr(mongo.db, model_class._collection_).remove({"_id" : ObjectId(object_id)})

 
class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(json.dumps(dict(*args, **kwargs), cls=MongoJsonEncoder), mimetype='application/json')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# TODO Why is this in "helpers" -- this should only be for common api requirements I think...
def upload_file(id, artist=None):
    file = request.files['file']
    imagedir = current_app.config['UPLOAD_FOLDER']
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = original_filename.split('.')[-1]
        original_image = os.path.join(imagedir, original_filename)
        file.save(original_image)

        web_image = os.path.join(imagedir, "%s_web.%s" % (id, extension))
        copyright_image = os.path.join(imagedir, "%s_copyright.png" % id)
        new_image = os.path.join(imagedir, "%s.%s" % (id, extension))
        tn_image = os.path.join(imagedir, "%s_tn.%s" % (id, extension))

        # Make Thumbnail of original
        shrink(original_image, 100, tn_image)

        # Make WaterMarked Image
        shrink(original_image, 600, web_image)
        copyrightText = "All Rights Reserved by artist"
        if artist:
            copyrightText = "Copyright %s" % artist
        create_copyright(copyrightText, copyright_image)
        watermark(web_image, copyright_image, new_image)

        # QR Code Image Creation
        # TODO QR Code Generation should happen only on initial creation of Art entity.
        baseUrl = current_app.config['API_BASE_URL']
        try:
            url = getShortURL("%s/art/%s/view" % (baseUrl, id))
            genQRcode(url, "%s/%s_qr.png" % (imagedir, id))
            # TODO add logging for art and URL
            # TODO store short URL for art entity
        except:
            # TODO add logging about failure
            pass

        # Remove the original and two temporary files
        os.remove(original_image)
        os.remove(web_image)
        os.remove(copyright_image)
        return True
    return False



