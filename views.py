from flask import render_template, url_for, request, session, redirect
from flask.ext.restful import Resource, Api

from api.artists import Artists
from api.art import Art
from api.artList import ArtList
from api.artImage import get_image
from api.venues import Venues, VenueList
from api.events import Event, EventList
from api.manage import ManageEvent, ManageVenue, ManagePerson
from api.staff import Staff, StaffList
from api.profile import Profile
from api.register import Register
from api.artistlist import ArtistList

from app import app, db
import model


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    return render_template('index.html')

# todo: Should route for OpenID Connect Authn
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/api/v1/art/<string:art_id>/<string:action_type>', methods=['GET'])
def render_image(art_id, action_type):
    return get_image(art_id, action_type)

# todo: Should route for OpenID Connect Logout


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

api = Api(app)

api.add_resource(Art, '/api/v1/art/<string:art_id>/')
# api.add_resource(ArtImage,'/api/v1/art/<string:art_id>/<string:action_type>')
api.add_resource(ArtList, '/api/v1/art/')

api.add_resource(Artists, '/api/v1/artists/<string:artist_id>')
api.add_resource(ArtistList, '/api/v1/artists/')

api.add_resource(Register, '/api/v1/register/<string:token>', '/api/v1/register/')

api.add_resource(EventList, '/api/v1/events/')
api.add_resource(Event, '/api/v1/event/<string:event_id>')

api.add_resource(VenueList, '/api/v1/venues/')
api.add_resource(Venues, '/api/v1/venues/<string:venue_id>')

api.add_resource(Profile, '/api/v1/profile')
api.add_resource(StaffList, '/api/v1/staff/')
api.add_resource(Staff, '/api/v1/staff/<string:person_id>')
api.add_resource(ManageEvent, '/api/v1/manage/events/', '/api/v1/manage/events/<string:event_id>')
api.add_resource(ManageVenue, '/api/v1/manage/venues/', '/api/v1/manage/venues/<string:venue_id>')
api.add_resource(ManagePerson, '/api/v1/manage/persons/', '/api/v1/manage/persons/<string:person_id>')
