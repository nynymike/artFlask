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
		if not args[a]:
			remove_parameters.append(a)
	for a in remove_parameters:
		del args[a]
	return args

def update_from_dictionary(data,item,model_class,object_id=None):
	for field in data:
		setattr(item,field,data[field])
	if object_id is None:
		 return getattr(mongo.db,model_class._collection_).save(item.to_dict())
	else:
		 return getattr(mongo.db,model_class._collection_).update({'_id': ObjectId(object_id)},{"$set": item.to_dict()},upsert=False)	

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


def upload_file(id):
	file = request.files['file']
	if file and allowed_file(file.filename):
	    filename = secure_filename(file.filename)
	    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
	    file.save(file_path)
	    extension = file_path.split('.')[-1]
	    copyright_image = current_app.config['UPLOAD_FOLDER'] + 'watermark.png'
	    create_copyright("copyright Michael Schwartz", copyright_image)
	    shrink(file_path, 600, "%s/thumb-%s.%s"%(current_app.config['UPLOAD_FOLDER'],id,extension))
	    watermark(file_path,copyright_image,"%s/web-%s.%s"%(current_app.config['UPLOAD_FOLDER'],id,extension))
	    os.remove(file_path)
	    return True
	return False




