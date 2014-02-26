from ..tests import TestCase
from ..tests.data.helpers import genArt, genVenue, genPerson
import json
from model import *
from bson import ObjectId
from db import mongo

class ArtTest(TestCase):

	# def test_show(self):
	# 	#self._test_get_request('/api/v1/artists/')

	def test_art(self):
		art = genArt(self.artist_id,self.venue_id)
		id = self._test_post_request('/api/v1/art/',data=json.dumps(art),model_class = ArtWork)
		self._test_get_request('/api/v1/art/%s/'%id)
		art = genArt(self.artist_id,self.venue_id)
		self._test_put_request('/api/v1/art/%s/'%id,data=json.dumps(art),model_class = ArtWork,id = id)
		self._test_put_delete('/api/v1/art/%s/'%id, model_class = ArtWork,id = id)

		'''
		Get ID 
		Send ID to get endpoint
		assert startus 200
		check len 1
		'''

		'''
		generate new art
		send update request to oid
		check for fields
		'''

		'''
		delete oid
		check in DB
		.count()
		'''

	def test_venue(self):
		venue = genVenue(artists = ["%s"%self.artist_id],managers =["%s"%self.artist_id])
		id = self._test_post_request('/api/v1/manage/venue',data=json.dumps(venue),model_class = Venue)
		self._test_get_request('/api/v1/venues/%s'%id)
		venue = genVenue(artists = ["%s"%self.artist_id],managers =["%s"%self.artist_id])
		self._test_put_request('/api/v1/manage/venue/%s'%id,data=json.dumps(venue),model_class = Venue,id = id)
		self._test_put_delete('/api/v1/manage/venue/%s'%id, model_class = Venue,id = id)



	def test_artist(self):
		artist = genPerson('artist')
		email = artist["email"]
		artist = json.dumps(artist)
		response_valid = self.client.post("/api/v1/register/",data = artist,  content_type='application/json')
		self.assertEqual(response_valid.status_code,200)
		response = self.client.post("/api/v1/register/",data = artist,  content_type='application/json')
		self.assertEqual(response.status_code,406)
		item = getattr(mongo.db,Person._collection_).find_one({"email":email})
		artist = genPerson('artist')
		self._test_put_request('/api/v1/manage/person/%s'%item['_id'],data=json.dumps(artist),model_class = Person,id = item['_id'])
		self._test_put_delete('/api/v1/manage/person/%s'%item['_id'], model_class = Person,id = item['_id'])




	def test_post_event(self):
		event = {
		'name': 'Happy Tour 2014',
		'startDate': 'Feb  3 00:00:00 UTC 2014',
		'endDate': 'Feb  5 00:00:00 UTC 2014',
		'description': 'This is a tour of all the artwork that you would want to see to make you smile',
		'picture': 'http://aloft.gluu.org/images/happy2014.png'
		}
		id = self._test_post_request('/api/v1/manage/event',data=json.dumps(event),model_class = Event)
		self._test_get_request('/api/v1/event/%s'%id)
		
		event = {
		'name': 'Happy Tour 2015',
		'startDate': 'Feb  4 00:00:00 UTC 2014',
		'endDate': 'Feb  6 00:00:00 UTC 2014',
		'description': 'This is a tour of all the artwork',
		'picture': 'http://aloft.gluu.org/images2/happy2014.png'
		}

		self._test_put_request('/api/v1/manage/event/%s'%id,data=json.dumps(event),model_class = Event,id = id)
		self._test_put_delete('/api/v1/manage/event/%s'%id, model_class = Event,id = id)



