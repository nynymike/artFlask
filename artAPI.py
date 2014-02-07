from flask import Flask
from flask.ext.restful import Resource, Api
from api.artists import Artists
from api.art import Art
from api.venues import Venues
from api.events import Events
from api.manage import ManageEvent, ManageVenue, ManagePerson
from api.staff import Staff
from api.profile import Profile

class Homepage(Resource):
    def get(self):
        return """
        ______________________
       |                     |
       | (____)              |
       |  (oo)               |
       |---\/           /----|
       |  ||           / |   |
       |--||          *  ||--|
       |  ^^             ^^  |
       |---------------------|
       1       artFlask      1
       """

UPLOAD_FOLDER = "C:\\Users\\mike\\Documents\\GitHub\\artFlask\\upload"
MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # 4MB max upload size

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

api = Api(app)
api.add_resource(Homepage, '/')
api.add_resource(Art, '/api/v1/art/<string:artist_id>',
                 '/api/v1/art/<string:artist_id>/<string:action_type>')
api.add_resource(Profile, '/api/v1/profile')
api.add_resource(Artists, '/api/v1/artists/<string:artist_id>')
api.add_resource(Staff, '/api/v1/staff', '/api/v1/staff/<string:staff_id>')
api.add_resource(Events, '/api/v1/events/<string:event_id>')
api.add_resource(Venues, '/api/v1/venues/<string:venue_id>')
api.add_resource(ManageEvent, '/api/v1/manage/event')
api.add_resource(ManageVenue, '/api/v1/manage/venue')
api.add_resource(ManagePerson, '/api/v1/manage/person')

if __name__ == '__main__':
    app.run(debug=True)