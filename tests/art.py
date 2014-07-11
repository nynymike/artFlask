import json

from . import TestCase
from factories import ArtworkFactory, VenueFactory

from app import db
from model import Artwork


class ArtTest(TestCase):
    API_URL = '/api/v1/art/'

    def test_empty_artlist(self):
        """
        Test empty request, empty response
        :return:
        """
        response = self.client.get(self.API_URL)
        self.assert403(response)
        args = {
            'title': 'Artwork!'
        }
        response = self.client.get(self.API_URL, query_string=args)
        self.assert404(response)

    def test_single_artwork(self):
        ArtworkFactory(parent_work=None)
        db.session.commit()

        response = self.client.get(self.API_URL, query_string={'medium': "Sculpture"})
        self.assert404(response)

        response = self.client.get(self.API_URL, query_string={'medium': "Painting"})
        self.assert200(response)
        data = json.loads(response.data)
        self.assertIn('item_list', data)
        self.assertEqual(len(data['item_list']), 1)
        artwork = data['item_list'][0]
        self.assertIsNotNone(artwork.get('artist'))
        self.assertEqual(u'Austin Sunrise', artwork.get('title'))
        self.assertEqual(u'Third in a series of 90 painting of the beautiful Austin skyline',
                         artwork.get('description'))
        self.assertEqual(u'http://auction.com/item/3432840932', artwork.get('buy_url'))
        self.assertIn('venue', artwork)
        self.assertEqual('Painting', artwork.get('medium'))
        self.assertFalse(artwork.get('sold_out'))

        self.assertEqual([], artwork.get('series'))
        self.assertIsNone(artwork.get('parent_work'))

        self.assertEqual(24, artwork.get('height'))
        self.assertEqual(34, artwork.get('width'))

        self.assertEqual(2014, artwork.get('year'))

        self.assertDictEqual({
                'Detail': 'http://goo.gl/23A3fi',
                'Back': 'http://goo.gl/xc3wyo',
            },
            artwork.get('alt_urls', {}))

    def test_add_artwork(self):
        VenueFactory(id=5)
        data = {
            # 'file': art_image,
            'title': u'Austin Sunrise',
            'description': u'Third in a series of 90 painting of the beautiful Austin skyline',
            'buy_url': u'http://auction.com/item/3432840932',
            'venue': 5,
            'medium': 'Painting',
            'sold': False,
            'series': [],
            'parent_work': None,
            'alt_urls': {
                'Detail': 'http://goo.gl/23A3fi',
                'Back': 'http://goo.gl/xc3wyo',
            },
        }
        self.assertEqual(0, Artwork.query.count())
        response = self.client.post(self.API_URL, data=json.dumps(data),
                                    follow_redirects=True, content_type='application/json')
        artwork = Artwork.query.first()
        self.assertIsNotNone(artwork)
        self.assertEqual(u'Austin Sunrise', artwork.title)
        self.assertEqual(u'Third in a series of 90 painting of the beautiful Austin skyline',
                         artwork.description)
        self.assertEqual(u'http://auction.com/item/3432840932', artwork.buy_url)
        self.assertEqual(1, artwork.venue_id)
        self.assertEqual('Painting', artwork.medium)
        self.assertFalse(artwork.sold_out)
        self.assertListEqual([], artwork.series)
        self.assertIsNone(artwork.parent_work)
        self.assertDictEqual({
            'Detail': 'http://goo.gl/23A3fi',
            'Back': 'http://goo.gl/xc3wyo',
        }, {u.name: u.url for u in artwork.alt_urls})
        self.assert201(response)


    # def test_art(self):
    #     """
    #     Test Case:
    #     1)Creates an Art object
    #     2)Inserts it into Database through Post request
    #     3)Fetches the same object through get request.
    #     4)Makes Some Changes to the object.
    #     5)Update the Object in database through PUT Request.
    #     6)Delete Object through Delete Request
    #     """
    #
    #     # art = genArt(self.artist_id, self.venue_id)
    #     # id = self._test_post_request('/api/v1/art/', data=json.dumps(art), model_class=Artwork)
    #     # self._test_get_request('/api/v1/art/%s/' % id)
    #     # art = genArt(self.artist_id, self.venue_id)
    #     # self._test_put_request('/api/v1/art/%s/' % id, data=json.dumps(art), model_class=Artwork, id=id)
    #     # self._test_put_delete('/api/v1/art/%s/' % id, model_class=Artwork, id=id)
    #
    # def test_venue(self):
    #     """
    #     Test Case:
    #     1)Creates an Venue object
    #     2)Inserts it into Database through Post request
    #     3)Fetches the same object through get request.
    #     4)Makes Some Changes to the object.
    #     5)Update the Object in database through PUT Request.
    #     6)Delete Object through Delete Request
    #     """
    #
    #     venue = genVenue(artists=["%s" % self.artist_id],
    #                      managers=["%s" % self.artist_id],
    #                      event_id=self.event_id)
    #     event_id = self._test_post_request('/api/v1/manage/venue',
    #                                        data=json.dumps(venue),
    #                                        model_class=Venue)
    #     self._test_get_request('/api/v1/venues/%s' % event_id )
    #     venue = genVenue(artists=["%s" % self.artist_id],
    #                      managers=["%s" % self.artist_id],
    #                      event_id=self.event_id)
    #     self._test_put_request('/api/v1/manage/venue/%s' % event_id,
    #                            data=json.dumps(venue),
    #                            model_class=Venue,
    #                            id=event_id)
    #     self._test_put_delete('/api/v1/manage/venue/%s' % event_id,
    #                           model_class=Venue,
    #                           id=event_id)
    #
    # def test_artist(self):
    #     """
    #     Test Case:
    #     1)Creates an Person object
    #     2)Inserts it into Database through Post request
    #     3)Fetches the same object through get request.
    #     4)Makes Some Changes to the object.
    #     5)Update the Object in database through PUT Request.
    #     6)Delete Object through Delete Request
    #     """
    #
    #     artist = genPerson('artist')
    #     email = artist["email"]
    #     artist = json.dumps(artist)
    #     response_valid = self.client.post("/api/v1/register/", data=artist, content_type='application/json')
    #     self.assertEqual(response_valid.status_code, 200)
    #     response = self.client.post("/api/v1/register/", data=artist, content_type='application/json')
    #     self.assertEqual(response.status_code, 406)
    #     item = getattr(mongo.db, Person._collection_).find_one({"email": email})
    #     artist = genPerson('artist')
    #     self._test_put_request('/api/v1/manage/person/%s' % item['_id'], data=json.dumps(artist), model_class=Person,
    #                            id=item['_id'])
    #     self._test_put_delete('/api/v1/manage/person/%s' % item['_id'], model_class=Person, id=item['_id'])
    #
    # def test_post_event(self):
    #     """
    #     Test Case:
    #     1)Creates an Event object
    #     2)Inserts it into Database through Post request
    #     3)Fetches the same object through get request.
    #     4)Makes Some Changes to the object.
    #     5)Update the Object in database through PUT Request.
    #     6)Delete Object through Delete Request
    #     """
    #
    #     event = {
    #         'name': 'Happy Tour 2014',
    #         'startDate': 'Feb  3 00:00:00 UTC 2014',
    #         'endDate': 'Feb  5 00:00:00 UTC 2014',
    #         'description': 'This is a tour of all the artwork that you would want to see to make you smile',
    #         'picture': 'http://aloft.gluu.org/images/happy2014.png'
    #     }
    #     event_id = self._test_post_request('/api/v1/manage/event',
    #                                        data=json.dumps(event),
    #                                        model_class=Event)
    #     self._test_get_request('/api/v1/event/%s' % event_id)
    #
    #     event = {
    #         'name': 'Happy Tour 2015',
    #         'startDate': 'Feb  4 00:00:00 UTC 2014',
    #         'endDate': 'Feb  6 00:00:00 UTC 2014',
    #         'description': 'This is a tour of all the artwork',
    #         'picture': 'http://aloft.gluu.org/images2/happy2014.png'
    #     }
    #
    #     self._test_put_request('/api/v1/manage/event/%s' % event_id,
    #                            data=json.dumps(event),
    #                            model_class=Event,
    #                            id=event_id)
    #     self._test_put_delete('/api/v1/manage/event/%s' % event_id,
    #                           model_class=Event,
    #                           id=event_id)

