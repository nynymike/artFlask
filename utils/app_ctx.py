from model.Art import ArtWork
from model.Venue import Venue
from model.Event import Event
from model.Person import Person
from utils.helpers import request_to_dictonary, update_from_dictionary,remove_record_by_id
from flask import request
from db import mongo
from bson import ObjectId
MODEL_MAP = {
    "art" : ArtWork,
    "venue" : Venue,
    "event" : Event,
    "person" : Person
}

class ApplicationContext(object):

<<<<<<< HEAD
	def query_from_context(self):
		model_class = self.model_class()
		data = request_to_dictonary(model_class)
		return self.query(**data)
=======
    def __init__(self,model_name):
        self.model_name = model_name
>>>>>>> 7731906a0b0cc75864146b15c92ba630e3baab82

    def create_item_from_context(self,object_id=None):
        model_class = self.model_class()
        item = model_class()
        data = request_to_dictonary(model_class)
        return  update_from_dictionary(data,item,model_class,object_id)


<<<<<<< HEAD
	def create_item_from_context(self,object_id=None):
		model_class = self.model_class()
		item = model_class()
		data = request_to_dictonary(model_class)
		return  update_from_dictionary(data,item,model_class,object_id)


	def model_class(self):
		return MODEL_MAP[self.model_name]

	def get_item(self,id=None):
		if id is None :
			item = getattr(mongo.db,self.model_class()._collection_).find({})
		else :
			item = getattr(mongo.db,self.model_class()._collection_).find({"_id":ObjectId(id)})
		return item.next()

	def query(self,**kwargs):
		print kwargs
		items = getattr(mongo.db,self.model_class()._collection_).find({})
		return items


	def remove_record(self,object_id):
		model_class = self.model_class()
		remove_recorde_by_id(object_id,model_class)
=======
    def model_class(self):
        return MODEL_MAP[self.model_name]
>>>>>>> 7731906a0b0cc75864146b15c92ba630e3baab82

    def get_item(self,id=None):
        if id is None :
            item = getattr(mongo.db,self.model_class()._collection_).find({})
        else :
            item = getattr(mongo.db,self.model_class()._collection_).find({"_id":ObjectId(id)})
        return item.next()

    def remove_record(self,object_id):
        model_class = self.model_class()
        remove_record_by_id(object_id, model_class)

    def search(self, d):
        return getattr(mongo.db,self.model_class()._collection_).find(`d`)

