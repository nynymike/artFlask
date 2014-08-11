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
from flask_restful_swagger import swagger

from sqlalchemy.exc import IntegrityError

from model import *
from app import db
from . import *


class ManageEvent(Resource):
    """
    Management API
    """
    MODEL = Event

    @swagger.operation(
        summary='update an event',
        responseClass=MODEL.__name__,
        nickname='update',
        parameters=[
            {
                'name': 'event_id',
                'dataType': 'integer',
                'description': 'event identifier',
                'required': True,
            }
        ]
    )
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

    @swagger.operation(
        method='POST',
        summary="create an event",
        notes="",
        type='void',
        responseClass=MODEL.__name__,
        nickname='createEvent',
        # "authorizations": {
        # "oauth2": [
        #     {
        #         "scope": "test:anything",
        #         "description": "anything"
        #     }
        # ]
        parameters=[
            {
                "name": "body",
                "description": "event to add",
                "required": True,
                "type": MODEL.__name__,
                "paramType": "body"
            }
        ],
        # responseMessages=[
        #     {
        #         "code": 400,
        #         "message": "Invalid event"
        #     }
        # ]
    )
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

    @swagger.operation(
        summary='delete an event',
        responseClass=MODEL.__name__,
        nickname='deleteEvent',
        parameters=[
            {
                'name': 'event_id',
                'dataType': 'integer',
                'description': 'event identifier',
                'required': True,
            }
        ]
    )
    def delete(self, event_id):
        o = self.MODEL.query.get(event_id)
        if not o:
            abort(404)
        db.session.delete(o)
        db.session.commit()


class ManageVenue(Resource):
    MODEL = Venue
    # REQUIRED = ["street", "city", "state", "zip"]

    @swagger.operation(
        summary='update a venue',
        responseClass=MODEL.__name__,
        nickname='updateVenue',
        parameters=[
            {
                'name': 'venue_id',
                'dataType': 'integer',
                'description': 'venue identifier',
                'required': True,
            }
        ]
    )
    def put(self, venue_id):
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

    @swagger.operation(
        summary='create a venue',
        responseClass=MODEL.__name__,
        nickname='createVenue',
        parameters=[]
    )
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

    @swagger.operation(
        summary='delete a venue',
        responseClass=MODEL.__name__,
        nickname='deleteVenue',
        parameters=[
            {
                'name': 'venue_id',
                'dataType': 'integer',
                'description': 'venue identifier',
                'required': True,
            }
        ]
    )
    def delete(self, venue_id):
        obj = self.MODEL.query.get(venue_id)
        if not obj:
            abort(404)
        db.session.delete(obj)
        db.session.commit()


class ManagePerson(Resource):
    MODEL = Person

    # Send SCIM requests to oxTrust
    @swagger.operation(
        summary='update a person',
        responseClass=MODEL.__name__,
        nickname='updatePerson',
        parameters=[
            {
                'name': 'person_id',
                'dataType': 'string',
                'description': 'openid identifier',
                'required': True,
            }
        ]
    )
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

    @swagger.operation(
        summary='delete a person',
        responseClass=MODEL.__name__,
        nickname='deletePerson',
        parameters=[
            {
                'name': 'person_id',
                'dataType': 'string',
                'description': 'openid identifier',
                'required': True,
            }
        ]
    )
    def delete(self, person_id):
        obj = self.MODEL.query.get(person_id)
        if not obj:
            abort(404)
        db.session.delete(obj)
        db.session.commit()

