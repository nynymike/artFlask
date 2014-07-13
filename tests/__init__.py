import sys
import os

from flask.ext.testing import TestCase as TestCaseBase, Twill
sys.path.append("%s/../" % os.getcwd())

from app import app, db

import logging
logging.getLogger('factory').setLevel(logging.WARN)


class ModelMixin:
    MODEL = None

    def assertObjectCount(self, count):
        self.assertEqual(count, self.MODEL.query.count())


class TestCase(TestCaseBase, ModelMixin):
    """Base TestClass for your application."""

    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test.db"
    TESTING = True
    maxDiff = None

    def create_app(self):
    #     """Create and return a testing flask app."""
    #
    #     app = Flask("test")
        app.testing = True
        # self.app = app.test_client()
        # app.config.from_object(TestingConfig)
    #     self._ctx = None
    #     self.app = app
    #     self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        db.create_all()
    #     self.artist = h.genPerson('artist')
    #     self.artist_id = "%s"%mongo.db.Person.save(self.artist)
    #     self.event = h.event
    #     self.event_id = "%s"%mongo.db.Event.save(self.event)
    #     self.venue = h.genVenue(["%s"%self.artist_id],["%s"%self.artist_id],event_id=self.event_id)
    #     self.venue_id ="%s"%mongo.db.Venue.save(self.venue)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assert201(self, response):
        """
        Checks if response status code is 201

        :param response: Flask response
        """

        self.assertStatus(response, 201)

    #     """Clean db session and drop all tables."""
    #     mongo.cx.drop_database(TestingConfig.MONGO_DBNAME)

    # def _test_get_request(self,endpoint,template=None):
    #     response = self.client.get(endpoint)
    #     self.assertEqual(response.status_code,200)
    #     data = json.loads(response.data)
    #     if template:
    #         self.assertTemplateUsed(name=template)
    #     return response
    #
    # def _test_post_request(self,endpoint,data,model_class):
    #     """
    #     Post Object through Post Request and returns object Id
    #     """
    #     response = self.client.post(endpoint, data=data,  content_type='application/json')
    #     self.assertEqual(response.status_code,201)
    #     oid = "%s"%response.data
    #     oid = oid.strip()[1:-1]
    #     id = ObjectId(oid)
    #     data = json.loads(data)
    #     data.pop("id",None)
    #     item = getattr(mongo.db,model_class._collection_).find({"_id":id}).next()
    #     for field in data:
    #         self.assertEqual(item[field],data[field])
    #     return id
    #
    # def _test_put_request(self,endpoint,data,model_class,id):
    #     """
    #     Update Object through Put Request
    #     """
    #     response = self.client.put(endpoint, data=data, content_type='application/json')
    #     if response.status_code != 200:
    #         import ipdb; ipdb.set_trace()
    #     self.assertEqual(response.status_code, 200)
    #     id = ObjectId(id)
    #     data = json.loads(data)
    #     data.pop("id",None)
    #     item = getattr(mongo.db,model_class._collection_).find({"_id":id}).next()
    #     for field in data:
    #         self.assertEqual(item[field],data[field])
    #
    # def _test_put_delete(self,endpoint,model_class,id):
    #     """
    #     Remove Object through Put Delete Request
    #     """
    #     response = self.client.delete(endpoint)
    #     self.assertEqual(response.status_code,200)
    #     id = ObjectId(id)
    #     item = getattr(mongo.db,model_class._collection_).find({"_id":id})
    #     self.assertEqual(item.count(),0)

