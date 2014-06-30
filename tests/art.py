import unittest
from . import TestCase
from .data.helpers import genArt, genVenue, genPerson
import json
from model import *
from bson import ObjectId
from db import mongo


class ArtTest(TestCase):
    # def test_show(self):
    # #self._test_get_request('/api/v1/artists/')

    def test_art(self):
        """
        Test Case:
        1)Creates an Art object
        2)Inserts it into Database through Post request
        3)Fetches the same object through get request.
        4)Makes Some Changes to the object.
        5)Update the Object in database through PUT Request.
        6)Delete Object through Delete Request
        """

        art = genArt(self.artist_id, self.venue_id)
        id = self._test_post_request('/api/v1/art/', data=json.dumps(art), model_class=ArtWork)
        self._test_get_request('/api/v1/art/%s/' % id)
        art = genArt(self.artist_id, self.venue_id)
        self._test_put_request('/api/v1/art/%s/' % id, data=json.dumps(art), model_class=ArtWork, id=id)
        self._test_put_delete('/api/v1/art/%s/' % id, model_class=ArtWork, id=id)

    def test_venue(self):
        """
        Test Case:
        1)Creates an Venue object
        2)Inserts it into Database through Post request
        3)Fetches the same object through get request.
        4)Makes Some Changes to the object.
        5)Update the Object in database through PUT Request.
        6)Delete Object through Delete Request
        """

        venue = genVenue(artists=["%s" % self.artist_id],
                         managers=["%s" % self.artist_id],
                         event_id=self.event_id)
        event_id = self._test_post_request('/api/v1/manage/venue',
                                           data=json.dumps(venue),
                                           model_class=Venue)
        self._test_get_request('/api/v1/venues/%s' % event_id )
        venue = genVenue(artists=["%s" % self.artist_id],
                         managers=["%s" % self.artist_id],
                         event_id=self.event_id)
        self._test_put_request('/api/v1/manage/venue/%s' % event_id,
                               data=json.dumps(venue),
                               model_class=Venue,
                               id=event_id)
        self._test_put_delete('/api/v1/manage/venue/%s' % event_id,
                              model_class=Venue,
                              id=event_id)

    def test_artist(self):
        """
        Test Case:
        1)Creates an Person object
        2)Inserts it into Database through Post request
        3)Fetches the same object through get request.
        4)Makes Some Changes to the object.
        5)Update the Object in database through PUT Request.
        6)Delete Object through Delete Request
        """

        artist = genPerson('artist')
        email = artist["email"]
        artist = json.dumps(artist)
        response_valid = self.client.post("/api/v1/register/", data=artist, content_type='application/json')
        self.assertEqual(response_valid.status_code, 200)
        response = self.client.post("/api/v1/register/", data=artist, content_type='application/json')
        self.assertEqual(response.status_code, 406)
        item = getattr(mongo.db, Person._collection_).find_one({"email": email})
        artist = genPerson('artist')
        self._test_put_request('/api/v1/manage/person/%s' % item['_id'], data=json.dumps(artist), model_class=Person,
                               id=item['_id'])
        self._test_put_delete('/api/v1/manage/person/%s' % item['_id'], model_class=Person, id=item['_id'])

    def test_post_event(self):
        """
        Test Case:
        1)Creates an Event object
        2)Inserts it into Database through Post request
        3)Fetches the same object through get request.
        4)Makes Some Changes to the object.
        5)Update the Object in database through PUT Request.
        6)Delete Object through Delete Request
        """

        event = {
            'name': 'Happy Tour 2014',
            'startDate': 'Feb  3 00:00:00 UTC 2014',
            'endDate': 'Feb  5 00:00:00 UTC 2014',
            'description': 'This is a tour of all the artwork that you would want to see to make you smile',
            'picture': 'http://aloft.gluu.org/images/happy2014.png'
        }
        event_id = self._test_post_request('/api/v1/manage/event',
                                           data=json.dumps(event),
                                           model_class=Event)
        self._test_get_request('/api/v1/event/%s' % event_id)

        event = {
            'name': 'Happy Tour 2015',
            'startDate': 'Feb  4 00:00:00 UTC 2014',
            'endDate': 'Feb  6 00:00:00 UTC 2014',
            'description': 'This is a tour of all the artwork',
            'picture': 'http://aloft.gluu.org/images2/happy2014.png'
        }

        self._test_put_request('/api/v1/manage/event/%s' % event_id,
                               data=json.dumps(event),
                               model_class=Event,
                               id=event_id)
        self._test_put_delete('/api/v1/manage/event/%s' % event_id,
                              model_class=Event,
                              id=event_id)


if __name__ == '__main__':
    unittest.main()
