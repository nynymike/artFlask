"""
.. currentmodule:: api.manage

Manage API
----------

   Functionality available to the tour admin. Access to ``/manage`` APIs are restricted
   to people with the ``staff`` value for user claim ``role``.

.. http:put:: /manage/event/(event_id)

   Update an event by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Event not found

.. http:post:: /manage/event

   Add a new event and return newly created event id. Returns new event id.

   :statuscode 201: Event Created
   :statuscode 404: Error creating event

.. http:delete:: /manage/event/(event_id)

   Delete an event.

   :statuscode 200: Event Deleted
   :statuscode 404: Not found

.. http:put:: /manage/venue/(venue_id)

    Update an venue by sending new JSON. See JSON schema for data format.

   :statuscode 200: no error
   :statuscode 404: Venue not found

.. http:post:: /manage/venue

   Add a new venue and return newly created venue id. See JSON schema for data format.
   No need to post venue id--it will be automatically generated.

   :statuscode 201: Venue Created
   :statuscode 404: Error creating Venue

.. http:delete:: /manage/venue/(venue_id)

    Delete a venue.

   :statuscode 200: no error
   :statuscode 404: Venue not found

.. http:put:: /manage/person/(person_id)

    Update a person by sending new JSON. See JSON schema for data format.
    SCIM update will be sent to oxTrust.

   :statuscode 200: no error
   :statuscode 404: Person not found

.. http:delete:: /manage/person/(person_id)

    Delete a person. SCIM update will be sent to oxTrust.

   :statuscode 200: no error
   :statuscode 404: Person not found

"""
__author__ = 'Michael Schwartz'

from datetime import datetime as dtime

from flask import request, abort
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from utils.app_ctx import ApplicationContext
from model import *
from app import db


class ManageEvent(Resource):
    MODEL = Event

    def put(self, event_id=None):
        try:
            print(event_id)
            app_ctx = ApplicationContext('Event')
            app_ctx.create_item_from_context(event_id)
            return '', 200
        except Exception as e:
            return '', 404

    def post(self):
        parser = reqparse.RequestParser()

        def date_from_str(s):
            return dtime.strptime(s, '%b %d %Y').date()
        for field in self.MODEL.__table__.columns:
            if field.type.python_type == date:
                parser.add_argument(field.name, type=date_from_str)
            else:
                parser.add_argument(field.name, type=field.type.python_type)
        args = {k: v for k, v in parser.parse_args(request).items() if v is not None}

        try:
            item = self.MODEL(**args)
            db.session.add(item)
            db.session.commit()
            return '%s' % item.id, 201
        except IntegrityError:
            abort(403)

    def delete(self, event_id=None):
        try:
            app_ctx = ApplicationContext('Event')
            app_ctx.remove_record(event_id)
            return '', 200
        except Exception as e:
            return '', 404


class ManageVenue(Resource):
    # REQUIRED = ["street", "city", "state", "zip"]

    # @staticmethod
    # def art_list_from_ids(ids):
    #     return Artwork.query.filter(Artwork.id.in_(ids)).all()

    #@cors.crossdomain(origin='*')
    def put(self, venue_id=None):
      try:
        app_ctx = ApplicationContext('Venue')
        item = app_ctx.create_item_from_context(venue_id)
        return '', 200
      except Exception as e:
        return '', 404

    # def post(self, venue_id=None):
    #     if not venue_id: return 'Venue not found', 404
    #     else:
    #         return None

    #@cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        for field in Venue.__table__.columns:
            parser.add_argument(field.name, type=field.type.python_type)

        def website_list_from_urls(urls):
            return [Website(name="url%d" % n, url=url) for n, url in enumerate(urls)]
        parser.add_argument('websites', type=website_list_from_urls)

        def mediums_from_names(names):
            return [Medium.query.get(name) or Medium(name=name) for name in names]
        parser.add_argument('mediums', type=mediums_from_names)

        def object_from_dict(class_name):
            def wrapper(d):
                return class_name(**d)
            return wrapper

        parser.add_argument('address', type=object_from_dict(Address))

        def objects_from_ids(class_name):
            def wrapper(lst):
                return [class_name.query.get(obj_id) for obj_id in lst]
            return wrapper
        parser.add_argument('artists', type=objects_from_ids(Person))
        parser.add_argument('managers', type=objects_from_ids(Person))

        def times_from_stringlist(stringlist):
            # TODO(analytic): move that to common place
            FORMAT = '%b %d %X %Z %Y'
            return [LimitedTime(start=dtime.strptime(start, FORMAT)) for start in stringlist]
        parser.add_argument('times', type=times_from_stringlist)

        args = {k: v for k, v in parser.parse_args(request).items() if v is not None}
        try:
            item = Venue(**args)
            db.session.add(item)
            db.session.commit()
            return '%s' % item.id, 201
        except IntegrityError:
            abort(403)
        # TODO(analytic): temporary disabled
        # app_ctx = ApplicationContext('Venue')
        # app_ctx.get_geo_location(item.id)

    #@cors.crossdomain(origin='*')
    def delete(self, venue_id=None):
        try:
            app_ctx = ApplicationContext('Venue')
            app_ctx.remove_record(venue_id)
            return '', 200
        except Exception as e:
            return '', 404


class ManagePerson(Resource):

    # Send SCIM requests to oxTrust
    #@cors.crossdomain(origin='*')
    def put(self, person_id=None):
        try:
            app_ctx = ApplicationContext('Person')
            app_ctx.create_item_from_context(person_id)
            return '', 200
        except Exception as e:
            return str(e),404

    #@cors.crossdomain(origin='*')
    def post(self, person_id=None):
        if not person_id: return 'Person not found', 404
        else:
            return None

    #@cors.crossdomain(origin='*')
    def delete(self, person_id=None):
      try:
        app_ctx = ApplicationContext('Person')
        app_ctx.remove_record(person_id)
        return '',200 
      except Exception as e:
        return '',404
