"""
.. currentmodule:: api.register

Register API
------------

   Registration workflow

.. http:post:: /register

   Send a Person entity to request registration. Check the Person Entity for
   required fields. A registration_code is generated and stored in the Person
   entity. The Person's status entry will be 'Pending' until the activation
   link is clicked.

   On registration, the person will be sent and email with
   an activation link.

   :statuscode 200: Registration request successful
   :statuscode 406: Duplicate registration

.. http:get:: /register/(registration_id)

   Validates the person's registration and asks them to choose a password.
   Sends a SCIM update to oxTrust to add the person for OpenID Connect
   authentication.

"""

__author__ = 'Michael Schwartz'

from datetime import datetime as dtime
from urlparse import urljoin

from bson.objectid import ObjectId
from utils.app_ctx import ApplicationContext
# from db import mongo
from flask.ext.mail import Message
from flask import current_app, request, abort
from mail import mail
# from flask_restful.utils import cors
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from model import RegistrationCode, Person, Website, Address
from app import db


def object_from_dict(class_name):
    def wrapper(d):
        return class_name(**d)
    return wrapper


def website_from_dict(d):
    return [Website(name=k, url=v) for k, v in d.items()]


def website_list_from_dict(url_dict):
    return [Website(name=k, url=v) for k, v in url_dict.items()]


class Register(Resource):
    #@cors.crossdomain(origin='*')
    def post(self):
        required_fields = [
            'sub',
            'email',
            'given_name',
            'family_name',
            'phone_number',
        ]
        unique_fields = ['email']
        parser = reqparse.RequestParser()
        for field in Person.__table__.columns:
            if field.name != 'role':
                parser.add_argument(field.name, type=field.type.python_type)
        parser.add_argument('address', type=object_from_dict(Address))
        parser.add_argument('website', type=website_from_dict)
        parser.add_argument('social_urls', type=website_list_from_dict)

        args = {k: v for k, v in parser.parse_args(request).items() if v is not None}
        args.update({
            'status': 'pending',
            'registration_code': RegistrationCode(sent=dtime.now()),
        })
        try:
            p = Person(**args)
            db.session.add(p)
            db.session.commit()
        except IntegrityError:
            abort(403)

        url = urljoin(current_app.config['BASE_URL'],
                      "api/v1/register/%s" % p.registration_code.hashed_id())
        html = u"Please click <a href='%s'>here</a> to verify your email address"\
               u" or copy paste %s in browser" % (url, url)
        message = Message(subject=u'Verify your email address',
                          html=html,
                          recipients=[p.email],
                          sender=current_app.config['DEFAULT_MAIL_SENDER'])
        mail.send(message)
        return '', 200

    #@cors.crossdomain(origin='*')
    def get(self, token):
        # FIXME(analytic): ineffective, store hashed ids in DB as well
        persons = Person.query.all()
        for p in persons:
            if token == p.registration_code.hashed_id():
                break
        else:
            abort(404)

        p.status = 'active'
        db.session.commit()

