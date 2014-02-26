from ..tests import TestCase
from ..tests.data.helpers import genArt, genVenue, genPerson
import json
from model import *
class ArtTest(TestCase):

	def test_show(self):
		self._test_get_request('/api/v1/artists/')

	def test_post_art(self):
		art = genArt(self.artist_id,self.venue_id)
		respose = self._test_post_request('/api/v1/art/',data=json.dumps(art),model_class = ArtWork)

	def test_post_venue(self):
		venue = genVenue(artists = ["%s"%self.artist_id],managers =["%s"%self.artist_id])
		print venue
		print "ahsan"
		respose = self._test_post_request('/api/v1/manage/venue',data=json.dumps(venue),model_class = Venue)

	def test_post_artist(self):
		artist = genPerson('artist')
		artist = json.dumps(artist)
		response = self.client.post("/api/v1/register/",data = artist,  content_type='application/json')
		self.assertEqual(response.status_code,200)
		response = self.client.post("/api/v1/register/",data = artist,  content_type='application/json')
		self.assertEqual(response.status_code,406)

	def test_post_event(self):
		event = {
		'name': 'Happy Tour 2014',
		'startDate': 'Feb  3 00:00:00 UTC 2014',
		'endDate': 'Feb  5 00:00:00 UTC 2014',
		'description': 'This is a tour of all the artwork that you would want to see to make you smile',
		'picture': 'http://aloft.gluu.org/images/happy2014.png'
		}
		print event
		print "ahsan"
		respose = self._test_post_request('/api/v1/manage/event',data=json.dumps(event),model_class = Event)


