import json
from urlparse import urljoin

from . import TestCase
from .factories import VenueFactory, EventFactory, PersonFactory

from app import db
from model import Venue


class VenueTestCase(TestCase):
    API_URL = '/api/v1/venues/'
    MANAGE_API_URL = '/api/v1/manage/venues/'

    def test_empty_venue_list(self):
        """
        Test request with no venues in DB
        :return:
        """
        response = self.client.get(self.API_URL)
        self.assert404(response)

        response = self.client.get(urljoin(self.API_URL, '1/'))
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

        response = self.client.get(self.API_URL)
        self.assert200(response)
        data = json.loads(response.data)
        self.assertIn('item_list', data)
        self.assertEqual(1, len(data['item_list']))

        venue = data['item_list'][0]

        self.assertEqual('1c', venue['site_id'])
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
        self.assertEqual([u'http://www.venue.com'], venue['websites'])
        self.assertEqual(1, len(venue.get('managers', [])))
        self.assertTrue(venue['curated'])
        self.assertEqual([u'Mon Feb  3 12:00:00 2014', u'Mon Feb  3 14:00:00 2014'],
                         venue['times'])

    def test_add_venue(self):
        self.assertEqual(0, Venue.query.count())
        EventFactory(id=7)
        PersonFactory(sub='111', role='artist')
        PersonFactory(sub='222', role='staff')
        db.session.commit()
        data = {
            'site_id': '101c',
            'name': u'Gallery Happy',
            'event_id': 7,
            'picture': u'http://www.galleryhappy.com/logo.png',
            'address': {
                "street": u"621 East Sixth Street",
                "locality": u"Austin",
                "region": u"TX",
                "postal_code": 78701,
                "country": u"US"
            },
            'twitter': '@GalleryHappy',
            'email': 'info@galleryhappy.org',
            'phone': '+1 512-555-1212',
            'category': u'Artists & Studios',
            'mediums': ['Ceramics'],
            'description': u'Fun stuff made of clay by talented people.',
            'artists': ['111'],
            'websites': [u'http://www.galleryhappy.com', u'http://google.com'],
            'managers': ['222'],
            'curated': True,
            'times': ['Feb  3 12:00:00 UTC 2014', 'Feb  3 14:00:00 UTC 2014'],
            'ad_1': True,
            'ad_2': True,
            'ad_3': True,
            'ad_4': True,
            'ad_5': True,
            'ad_6': True,
            'ad_7': True,
            'ad_8': False,
        }
        self.client.post(self.MANAGE_API_URL, data=json.dumps(data),
                         follow_redirects=True, content_type='application/json')
        venue = Venue.query.first()
        self.assertIsNotNone(venue)
        self.assertEqual('101c', venue.site_id)
        self.assertEqual(u'Gallery Happy', venue.name)
        self.assertEqual(7, venue.event_id)
        self.assertEqual(u'http://www.galleryhappy.com/logo.png', venue.picture)
        self.assertDictEqual({
                "street": u"621 East Sixth Street",
                "locality": u"Austin",
                "region": u"TX",
                "postal_code": 78701,
                "country": u"US"
            },
            venue.address.as_dict())
        self.assertEqual('@GalleryHappy', venue.twitter)
        self.assertEqual('info@galleryhappy.org', venue.email)
        self.assertEqual('+1 512-555-1212', venue.phone)
        self.assertEqual(u'Artists & Studios', venue.category)
        self.assertListEqual(['Ceramics'], [m.name for m in venue.mediums])
        self.assertEqual(u'Fun stuff made of clay by talented people.', venue.description)
        self.assertListEqual(['111'], [a.sub for a in venue.artists])
        self.assertEqual([u'http://www.galleryhappy.com', u'http://google.com'],
                         [w.url for w in venue.websites])
        self.assertListEqual(['222'], [m.sub for m in venue.managers])
        self.assertEqual(True, venue.curated)
        # TODO(analytic): move to common time format ( 3 => 03)
        # TODO(analytic): UTC parsing ??
        self.assertEqual(['Feb 03 12:00:00 2014', 'Feb 03 14:00:00 2014'],
                         [t.start.strftime('%b %d %X %Y') for t in venue.times])
        self.assertTrue(venue.ad_1)
        self.assertTrue(venue.ad_2)
        self.assertTrue(venue.ad_3)
        self.assertTrue(venue.ad_4)
        self.assertTrue(venue.ad_5)
        self.assertTrue(venue.ad_6)
        self.assertTrue(venue.ad_7)
        self.assertFalse(venue.ad_8)
