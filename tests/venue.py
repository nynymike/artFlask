import json
from urlparse import urljoin

from app import db

from . import TestCase
from .factories import VenueFactory


class VenueTestCase(TestCase):
    BASE_API_URL = '/api/v1/venues/'

    def test_empty_venue_list(self):
        """
        Test request with no venues in DB
        :return:
        """
        response = self.client.get(self.BASE_API_URL)
        self.assert404(response)

        response = self.client.get(urljoin(self.BASE_API_URL, '1/'))
        self.assert404(response)

    def test_two_venues(self):
        VenueFactory.create_batch(2)

    def test_single_venue(self):
        """
        Test single venue
        :return:
        """
        VenueFactory(name=u'Venue1')
        db.session.commit()

        response = self.client.get(self.BASE_API_URL)
        self.assert200(response)
        data = json.loads(response.data)
        self.assertIn('item_list', data)
        self.assertEqual(1, len(data['item_list']))

        venue = data['item_list'][0]

        self.assertEqual('101c', venue['site_id'])
        self.assertEqual(u'Venue1', venue['name'])
        self.assertIsNotNone(venue.get('event'))
        self.assertEqual(u'http://www.galleryhappy.com/logo.png', venue['picture'])
        self.assertDictEqual(venue['address'], {
            u'country': u'US',
            u'region': u'TX',
            u'postal_code': 78701,
            u'street': u'621 East Sixth Street',
            u'locality': u'Austin',
            })
        self.assertAlmostEqual(40.446195, venue['latitude'], delta=0.01)
        self.assertAlmostEqual(-79.982195, venue['longitude'], delta=0.01)
        self.assertEqual('@GalleryHappy', venue['twitter'])
        self.assertEqual('info@galleryhappy.org', venue['email'])
        self.assertEqual('+1 512-555-1212', venue['phone'])
        self.assertEqual(u'Artists & Studios', venue['category'])
        self.assertEqual([u'Ceramics', u'Painting'], venue['mediums'])
        self.assertEqual(u'Fun stuff made of clay by talented people.', venue['description'])
        self.assertEqual(1, len(venue.get('artists', [])))
        self.assertEqual([u'http://www.galleryhappy.com'], venue['websites'])
        self.assertEqual(1, len(venue.get('managers', [])))
        self.assertTrue(venue['curated'])
        self.assertEqual([u'Mon Feb  3 12:00:00 2014', u'Mon Feb  3 14:00:00 2014'],
                         venue['times'])
