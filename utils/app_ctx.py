from model.Art import ArtWork
from model.Venue import Venue
from model.Event import Event
from model.Person import Person
from utils.helpers import request_to_dictonary, update_from_dictionary,remove_record_by_id
from flask import request
from mainapp import mongo
from bson import ObjectId
MODEL_MAP = {
    "art" : ArtWork,
    "venue" : Venue,
    "event" : Event,
    "person" : Person
}

class ApplicationContext(object):

    def __init__(self,model_name):
        self.model_name = model_name

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

    def remove_record(self,object_id):
        model_class = self.model_class()
        remove_record_by_id(object_id, model_class)

    def search(self, d):
        return getattr(mongo.db,self.model_class()._collection_).find(`d`)

