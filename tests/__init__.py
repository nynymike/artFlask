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
    maxDiff = None  # helpful to compare big dicts

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assert201(self, response):
        """
        Checks if response status code is 201

        :param response: Flask response
        """

        self.assertStatus(response, 201)

