from flask.ext.restful import reqparse
from flask import request
from mainapp import mongo
from bson.objectid import ObjectId
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        raise ImportError
import datetime
from werkzeug import Response

def request_to_dictonary(model_class):
	schema = model_class.schema
	parser = reqparse.RequestParser()
	print request.data
	for field in schema:
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
		getattr(mongo.db,model_class._collection_).save(item.to_dict())
	else:
		getattr(mongo.db,model_class._collection_).update({'_id': ObjectId(object_id)},{"$set": item.to_dict()},upsert=False)	

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