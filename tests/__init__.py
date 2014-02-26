from flask.ext.testing import TestCase as Base, Twill
import sys
import os
sys.path.append("%s/../"%os.getcwd())
from app import create_app
from conf import TestingConfig
from db import mongo
import data.helpers as h
from bson import ObjectId
import json
class TestCase(Base):
    """Base TestClass for your application."""

    def create_app(self):
        """Create and return a testing flask app."""

        app = create_app("test",TestingConfig)
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        self.artist = h.genPerson('artist')
        self.artist_id = "%s"%mongo.db.Person.save(self.artist)
        self.venue = h.genVenue(["%s"%self.artist_id],["%s"%self.artist_id])
        self.venue_id ="%s"%mongo.db.Venue.save(self.venue)



    def tearDown(self):
        """Clean db session and drop all tables."""
        mongo.cx.drop_database(TestingConfig.MONGO_DBNAME)



    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response

    def _test_post_request(self, endpoint,data,model_class):
        response = self.client.post(endpoint,data = data,  content_type='application/json')
        self.assertEqual(response.status_code,201)
        oid = "%s"%response.data
        oid = oid.strip()[1:-1]
        id = ObjectId(oid)
        data = json.loads(data)
        data.pop("id",None)
        item = getattr(mongo.db,model_class._collection_).find({"_id":id}).next()
        for field in data:
            self.assertEqual(item[field],data[field])





