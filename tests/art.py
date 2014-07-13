import json
from urlparse import urljoin

from . import TestCase
from factories import ArtworkFactory, VenueFactory

from app import db
from model import Artwork


class ArtTest(TestCase):
    API_URL = '/api/v1/art/'
    MANAGE_API_URL = '/api/v1/manage/art/'
    MODEL = Artwork
    FACTORY = ArtworkFactory

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
        self.assertEqual(0, Artwork.query.count())

        VenueFactory(id=5)
        db.session.commit()
        ArtworkFactory(id=5)
        db.session.commit()
        data = {
            # 'file': art_image,
            'title': u'Austin Sunrise Special',
            'description': u'Third in a series of 90 painting of the beautiful Austin skyline',
            'buy_url': u'http://auction.com/item/3432840932',
            'venue': 5,
            'medium': 'Painting',
            'sold': False,
            'series': [5],
            'parent_work': 5,
            'alt_urls': {
                'Detail': 'http://goo.gl/23A3fi',
                'Back': 'http://goo.gl/xc3wyo',
            },
        }
        response = self.client.post(self.API_URL, data=json.dumps(data),
                                    follow_redirects=True, content_type='application/json')
        artwork = Artwork.query.filter_by(title=u'Austin Sunrise Special').first()
        self.assertIsNotNone(artwork)
        self.assertEqual(u'Austin Sunrise Special', artwork.title)
        self.assertEqual(u'Third in a series of 90 painting of the beautiful Austin skyline',
                         artwork.description)
        self.assertEqual(u'http://auction.com/item/3432840932', artwork.buy_url)
        self.assertEqual(5, artwork.venue_id)
        self.assertEqual('Painting', artwork.medium)
        self.assertFalse(artwork.sold_out)
        self.assertListEqual([5], [s.id for s in artwork.series])
        self.assertEqual(5, artwork.parent_id)
        self.assertDictEqual({
            'Detail': 'http://goo.gl/23A3fi',
            'Back': 'http://goo.gl/xc3wyo',
        }, {u.name: u.url for u in artwork.alt_urls})
        self.assert201(response)

    def test_deletion(self):
        self.assertObjectCount(0)
        self.FACTORY(id=5)
        db.session.commit()
        self.assertObjectCount(1)
        self.client.delete(urljoin(self.API_URL, '%d/' % 5))
        self.assertObjectCount(0)

