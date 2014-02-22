from model.Art import ArtWork
from model.Venue import Venue
from model.Event import Event
from model.Person import Person
from utils.helpers import request_to_dictonary, update_from_dictionary,remove_record_by_id
from flask import request, abort
from db import mongo
from bson import ObjectId
MODEL_MAP = {
    "art" : ArtWork,
    "venue" : Venue,
    "event" : Event,
    "person" : Person
}

class ApplicationContext(object):


	def query_from_context(self,allowList=False):
		model_class = self.model_class()
		data = request_to_dictonary(model_class,typeSafe=False)
		if not data and not allowList:
			abort(501)
		return self.query(**data)

	def __init__(self,model_name):
		self.model_name = model_name


	def verify_data(self,data,required_fields,unique_fields):
		for field in required_fields:
			if not data.has_key(field):
				abort("%s is required"%field,400)
		for field in unique_fields:
			print data[field]
			item = getattr(mongo.db,self.model_class()._collection_).find({field:data[field]})
			if item.count() > 0:
				print "%s is already taken"%field
				abort(406)
		return True
	
	def create_item_from_context(self,object_id=None,required_fields=[],unique_fields=[]):
		model_class = self.model_class()
		item = model_class()
		data = request_to_dictonary(model_class)
		if object_id == None:
			self.verify_data(data,required_fields,unique_fields)
		return  update_from_dictionary(data,item,model_class,object_id)


	def model_class(self):
		return MODEL_MAP[self.model_name]

	def get_item(self,id=None):
		if id is None :
			item = getattr(mongo.db,self.model_class()._collection_).find({})
		else:
			item = getattr(mongo.db,self.model_class()._collection_).find({"_id":ObjectId(id)})
		return item.next()

	def query(self,**kwargs):
		print kwargs
		items = getattr(mongo.db,self.model_class()._collection_).find(kwargs)
		return items


	def remove_record(self,object_id):
		model_class = self.model_class()
		remove_record_by_id(object_id,model_class)


