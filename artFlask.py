from flask import Flask, url_for, request, session, redirect
from flask.ext.restful import Resource, Api
from api.artists import Artists
from api.art import Art
from api.venues import Venues
from api.events import Events
from api.manage import ManageEvent, ManageVenue, ManagePerson
from api.staff import Staff
from api.profile import Profile
from api.register import Register
from flask import render_template

UPLOAD_FOLDER = "C:\\Users\\mike\\Documents\\GitHub\\artFlask\\upload"
MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # 4MB max upload size

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = 'z\xcbu\xe5#\xf2U\xe5\xc4,\x0cz\xf9\xcboA\xd2Z\xf7Y\x15"|\xe4'

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

# todo: Should route for OpenID Connect Logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

api = Api(app)
api.add_resource(Register, '/api/v1/register', '/api/v1/register/<string:registration_id>')
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