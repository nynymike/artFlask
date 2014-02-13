from flask.ext.restful import reqparse
from flask import request
from mainapp import mongo

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

def update_from_dictionary(data,item,model_class):
	for field in data:
		setattr(item,field,data[field])
	getattr(mongo.db,model_class._collection_).save(item.to_dict())