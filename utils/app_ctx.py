from model import Artwork
from model.Venue import Venue
from model.Event import Event
from model.Person import Person
from utils.helpers import request_to_dictonary, update_from_dictionary # , remove_record_by_id
from flask import request, abort
from db import mongo
from bson import ObjectId
from api.venueFunctions import geoCode

MODEL_MAP = {
    "art": Artwork,
    "venue": Venue,
    "event": Event,
    "person": Person,
}


class ApplicationContext(object):
    def query_from_context(self, allowList=False, default_data=None):
        model_class = self.model_class()
        data = request_to_dictonary(model_class, typeSafe=False)
        if default_data:
            data.update(default_data)
        if not data and not allowList:
            abort(501)
        return self.query(**data)

    def __init__(self, model_name):
        self.model_name = model_name

    def verify_data(self, data, required_fields, unique_fields):
        for field in required_fields:
            if not self.myhaskey(d=data,key=field):
                abort(422, "%s is required" % field)
        for field in unique_fields:
            print(data[field])
            item = getattr(mongo.db, self.model_class()._collection_).find({field: data[field]})
            if item.count() > 0:
                #print "%s is already taken"%field
                abort(406)
        return True

    def create_item_from_context(self, object_id=None, required_fields=[], unique_fields=[]):
        model_class = self.model_class()
        item = model_class()
        data = request_to_dictonary(model_class)
        if object_id is None:
            self.verify_data(data=data,required_fields=required_fields,unique_fields=unique_fields)
        return update_from_dictionary(data,item,model_class,object_id)

    def model_class(self):
        return MODEL_MAP[self.model_name]

    def get_item(self, item_id=None):
        item = self.model_class().query.get(item_id)
        item_dict = item.__dict__.copy()
        return item_dict

    def query(self, **kwargs):
        items = self.model_class().query.filter_by(kwargs)
        return [item.__dict__.copy() for item in items]

    def remove_record(self, object_id):
        model_class = self.model_class()
        model_class.query.get(object_id).delete()
        # remove_record_by_id(object_id, model_class)

    def get_geo_location(self, item_id):
        try:
            model_class = self.model_class()
            item = self.get_item(item_id=item_id)
            address = item['address']
            geolocation = geoCode(street=address["street"],
                                  city=address["city"],
                                  state=address["state"],
                                  zip=address["zip"])
            item["coordinates"] = geolocation[0]
            item.pop("_id")
            return getattr(mongo.db, model_class._collection_).update({'_id': item_id},{"$set": item}, upsert=False)
        except Exception as e:
            return ''

    def myhaskey(self,d,key):
        return d.has_key(key) or any(self.myhaskey(d=dd,key=key) for dd in d.values() if isinstance(dd, dict))



