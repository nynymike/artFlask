from flask.ext.restful import reqparse
from flask import Flask, request, redirect, url_for, current_app
from db import mongo
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime
from werkzeug import Response
from api.artImageFunctions import shrink , watermark, create_copyright

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def request_to_dictonary(model_class,typeSafe=True):
	schema = model_class.schema
	parser = reqparse.RequestParser()
	for field in schema:
		if typeSafe:
			parser.add_argument(field,type=schema[field][type])
		else:
			parser.add_argument(field)
	args =  parser.parse_args(request)
	remove_parameters = []
	for a in args:
		if args[a] == None:
			remove_parameters.append(a)
	for a in remove_parameters:
		del args[a]
	return args

def update_from_dictionary(data,item,model_class,object_id=None):
	print "data"
	print data
	if object_id is None:
		 return getattr(mongo.db,model_class._collection_).save(data)
	else:
		 return getattr(mongo.db,model_class._collection_).update({'_id': ObjectId(object_id)},{"$set": data},upsert=False)	

def remove_record_by_id(object_id,model_class):
	getattr(mongo.db,model_class._collection_).remove({"_id" : ObjectId(object_id)})

 
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

def upload_file(id, artist=None):
    file = request.files['file']
    basedir = current_app.config['UPLOAD_FOLDER']
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        extension = original_filename.split('.')[-1]
        original_image = os.path.join(basedir, original_filename)
        file.save(original_image)

        web_image = os.path.join(basedir, "%s_web.%s" % (id, extension))
        copyright_image = os.path.join(basedir, "%s_copyright.png" % id)
        new_image = os.path.join(basedir, "%s.%s" % (id, extension))
        tn_image = os.path.join(basedir, "%s_tn.%s" % (id, extension))

        # Make Thumbnail of original
        shrink(original_image, 100, tn_image)

        # Make WaterMarked Image
        shrink(original_image, 600, web_image)
        copyrightText = "All Rights Reserved by artist"
        if artist:
            copyrightText = "Copyright %s" % artist
        create_copyright(copyrightText, copyright_image)
        watermark(web_image, copyright_image, new_image)

        # Remove the original and two temporary files
        os.remove(original_image)
        os.remove(web_image)
        os.remove(copyright_image)
        return True
    return False



