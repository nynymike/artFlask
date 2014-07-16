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


def date_from_str(s):
    return dtime.strptime(s, '%b %d %Y').date()


def website_list_from_urls(urls):
    return [Website(name="url%d" % n, url=url) for n, url in enumerate(urls)]


def website_list_from_dict(url_dict):
    return [Website(name=k, url=v) for k, v in url_dict.items()]


def mediums_from_names(names):
    return [Medium.query.get(name) or Medium(name=name) for name in names]


def object_from_dict(class_name):
    def wrapper(d):
        return class_name(**d)
    return wrapper


def objects_from_ids(class_name):
    def wrapper(lst):
        return [class_name.query.get(obj_id) for obj_id in lst]
    return wrapper


def times_from_stringlist(stringlist):
    # TODO(analytic): move that to common place
    FORMAT = '%b %d %X %Z %Y'
    return [LimitedTime(start=dtime.strptime(start, FORMAT)) for start in stringlist]


def website_from_dict(d):
    return [Website(name=k, url=v) for k, v in d.items()]


class ManageEvent(Resource):
    MODEL = Event

    def put(self, event_id):
        event = self.MODEL.query.get(event_id)
        if not event:
            abort(404)

        parser = reqparse.RequestParser()
        for field in self.MODEL.__table__.columns:
            if field.type.python_type == date:
                parser.add_argument(field.name, type=date_from_str)
            else:
                parser.add_argument(field.name, type=field.type.python_type)
        for k, v in parser.parse_args(request).items():
            if v is not None:
                setattr(event, k, v)
        db.session.commit()

    def post(self):
        parser = reqparse.RequestParser()

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

    def delete(self, event_id):
        o = self.MODEL.query.get(event_id)
        if not o:
            abort(404)
        db.session.delete(o)
        db.session.commit()


class ManageVenue(Resource):
    MODEL = Venue
    # REQUIRED = ["street", "city", "state", "zip"]

    def put(self, venue_id=None):
        venue = self.MODEL.query.get(venue_id)
        if not venue:
            abort(404)

        parser = reqparse.RequestParser()
        for field in self.MODEL.__table__.columns:
            parser.add_argument(field.name, type=field.type.python_type)

        parser.add_argument('websites', type=website_list_from_urls)

        parser.add_argument('mediums', type=mediums_from_names)

        parser.add_argument('address', type=object_from_dict(Address))

        parser.add_argument('artists', type=objects_from_ids(Person))
        parser.add_argument('managers', type=objects_from_ids(Person))

        parser.add_argument('times', type=times_from_stringlist)

        for k, v in parser.parse_args(request).items():
            if v is not None:
                setattr(venue, k, v)
        db.session.commit()

    # def post(self, venue_id=None):
    #     if not venue_id: return 'Venue not found', 404
    #     else:
    #         return None

    #@cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        for field in self.MODEL.__table__.columns:
            parser.add_argument(field.name, type=field.type.python_type)

        parser.add_argument('websites', type=website_list_from_urls)

        parser.add_argument('mediums', type=mediums_from_names)

        parser.add_argument('address', type=object_from_dict(Address))

        parser.add_argument('artists', type=objects_from_ids(Person))
        parser.add_argument('managers', type=objects_from_ids(Person))

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

    def delete(self, venue_id=None):
        obj = self.MODEL.query.get(venue_id)
        if not obj:
            abort(404)
        db.session.delete(obj)
        db.session.commit()


class ManagePerson(Resource):
    MODEL = Person

    # Send SCIM requests to oxTrust
    def put(self, person_id):
        person = self.MODEL.query.get(person_id)
        if not person:
            abort(404)

        parser = reqparse.RequestParser()
        for field in self.MODEL.__table__.columns:
            if field.name != 'role':
                parser.add_argument(field.name, type=field.type.python_type)
        parser.add_argument('address', type=object_from_dict(Address))
        parser.add_argument('website', type=website_from_dict)
        parser.add_argument('social_urls', type=website_list_from_dict)

        for k, v in parser.parse_args(request).items():
            if v is not None:
                setattr(person, k, v)
        db.session.commit()

    def delete(self, person_id):
        obj = self.MODEL.query.get(person_id)
        if not obj:
            abort(404)
        db.session.delete(obj)
        db.session.commit()

