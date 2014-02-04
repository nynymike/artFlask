from flask import Flask
from flask.ext.restful import Resource, Api
from api.artists import Artists
from api.art import Art
from api.venues import Venues
from api.events import Events
from api.manage import ManageEvent, ManageVenue, ManagePerson
from api.staff import Staff

class Homepage(Resource):
    def get(self):
        return "Welcome to the Art Tour API Server."

art = {}
event = {}
person = {}
venue = {}

app = Flask(__name__)
api = Api(app)
api.add_resource(Homepage, '/')
api.add_resource(Artists, '/api/v1/artists/<string:artist_id>')
api.add_resource(Events, '/api/v1/events/<string:event_id>')
api.add_resource(Venues, '/api/v1/venues/<string:venue_id>')
api.add_resource(Art, '/api/v1/art/<string:artist_id>',
                      '/api/v1/art/<string:artist_id>/<string:action_type>')
api.add_resource(Staff, '/api/v1/staff', '/api/v1/staff/<string:staff_id>')
api.add_resource(ManageEvent, '/api/v1/staff/event')
api.add_resource(ManageVenue, '/api/v1/staff/venue')
api.add_resource(ManagePerson, '/api/v1/staff/person')

if __name__ == '__main__':
    app.run(debug=True)