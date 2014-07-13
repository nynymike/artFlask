from utils.helpers import request_to_dictonary  # , update_from_dictionary, remove_record_by_id
from flask import abort
from api.venueFunctions import geoCode

from app import db
from importlib import import_module

# MODEL_MAP = {
#     "art": Artwork,
#     "venue": Venue,
#     "event": Event,
#     "person": Person,
# }


class ApplicationContext(object):
    def query_from_context(self, allowList=False, default_data=None):
        model_class = self.model_class()
        data = request_to_dictonary(model_class, typeSafe=False)

        if default_data:
            data.update(default_data)

        if not data and not allowList:
            # FIXME(analytic): description is not handled anywhere
            abort(403, description=u"Queries with no filtering params not allowed")
        result = list(self.query(**data))

        if not result:
            abort(404)

        return result

    def __init__(self, model_name):
        self.model_name = model_name

    # def verify_data(self, data, required_fields, unique_fields):
    #     for field in required_fields:
    #         if not self.myhaskey(d=data,key=field):
    #             abort(422, "%s is required" % field)
    #     for field in unique_fields:
    #         print(data[field])
    #         item = getattr(mongo.db, self.model_class()._collection_).find({field: data[field]})
    #         if item.count() > 0:
    #             #print "%s is already taken"%field
    #             abort(406)
    #     return True

    def create_item_from_context(self, object_id=None, required_fields=None, unique_fields=None):
        # required_fields = required_fields or []
        # unique_fields = unique_fields or []
        ModelClass = self.model_class()
        data = request_to_dictonary(ModelClass)
        # if object_id is None:
        #     self.verify_data(data=data, required_fields=required_fields, unique_fields=unique_fields)
        item = ModelClass(**data)
        db.session.add(item)
        db.session.merge(item)
        db.session.commit()
        # return update_from_dictionary(data, item, ModelClass, object_id)
        return item

    def model_class(self):
        # return MODEL_MAP[self.model_name]
        module = import_module('model')
        return getattr(module, self.model_name)

    def get_item(self, item_id=None):
        item = self.model_class().query.get(item_id)
        if not item:
            abort(404)
        item_dict = item.as_dict()
        return item_dict

    def query(self, **kwargs):
        return self.model_class().query.filter_by(**kwargs)

    def remove_record(self, object_id):
        model_class = self.model_class()
        model_class.query.get(object_id).delete()
        # remove_record_by_id(object_id, model_class)

    def get_geo_location(self, item_id):
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

    def myhaskey(self,d,key):
        return d.has_key(key) or any(self.myhaskey(d=dd,key=key) for dd in d.values() if isinstance(dd, dict))



