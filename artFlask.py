#!/usr/bin/python

from flask import Flask, url_for, request, session, redirect
from flask.ext.restful import Resource, Api
from api.artists import Artists
from api.art import Art
from api.artList import ArtList
from api.artImage import ArtImage
from api.venues import Venues,VenueList
from api.events import Events
from api.manage import ManageEvent, ManageVenue, ManagePerson
from api.staff import Staff,StaffList
from api.profile import Profile
from api.register import Register
from api.artistlist import ArtistList
from flask import render_template
import logging
from logging.handlers import RotatingFileHandler
import os, sys
sys.path.append(os.getcwd())
from flask import Flask
from db import mongo
from mail import mail

def create_app(name):
    app = Flask(name)
    app.name = "artFlask"
    app.config.from_object('conf')
    configure_logger(app)
    configure_routes(app)
    configure_extensions(app)
    return app

def configure_extensions(app):
    mongo.init_app(app)
    mail.init_app(app)

def configure_logger(app):

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # 4MB max upload size
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.secret_key = 'z\xcbu\xe5#\xf2U\xe5\xc4,\x0cz\xf9\xcboA\xd2Z\xf7Y\x15"|\xe4'

    logger = logging.getLogger('app')

    if app.config.has_key('LOGGING_FILE'):
        handler = RotatingFileHandler(app.config['LOGGING_FILE'],
                                          maxBytes=10000000,
                                          backupCount=5)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def configure_routes(app):

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/')
    def index():
        ## TESTING
        print "**********\n", mongo.db, "\n**********\n" 
        return render_template('index.html')

    # todo: Should route for OpenID Connect Authn
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    # todo: Should route for OpenID Connect Logout


    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('index'))

    api = Api(app)

    api.add_resource(Art,'/api/v1/art/<string:art_id>/')
    api.add_resource(ArtImage,'/api/v1/art/<string:art_id>/<string:action_type>')
    api.add_resource(ArtList,'/api/v1/art/')

    api.add_resource(Artists, '/api/v1/artists/<string:artist_id>')
    api.add_resource(ArtistList, '/api/v1/artists/')

    api.add_resource(Register, '/api/v1/register/<string:token>','/api/v1/register/')

    api.add_resource(Events, '/api/v1/events/')

    api.add_resource(VenueList, '/api/v1/venues')
    api.add_resource(Venues, '/api/v1/venues/<string:venue_id>')    

    api.add_resource(Profile, '/api/v1/profile')
    api.add_resource(StaffList, '/api/v1/staff/')
    api.add_resource(Staff, '/api/v1/staff/<string:person_id>')
    api.add_resource(ManageEvent, '/api/v1/manage/event','/api/v1/manage/event/<string:event_id>')
    api.add_resource(ManageVenue, '/api/v1/manage/venue','/api/v1/manage/venue/<string:venue_id>')
    api.add_resource(ManagePerson, '/api/v1/manage/person','/api/v1/manage/person/<string:person_id>')


if __name__ == '__main__':
    app = create_app(__name__)
    app.run(host='0.0.0.0',debug=True)
