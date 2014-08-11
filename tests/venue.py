import json
from datetime import datetime as dtime
from urlparse import urljoin

from . import TestCase
from .factories import VenueFactory, EventFactory, PersonFactory

from app import db
from model import Venue


class VenueTestCase(TestCase):
    API_URL = '/api/v1/venues/'
    MANAGE_API_URL = '/api/v1/manage/venues/'
    MODEL = Venue
    FACTORY = VenueFactory

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
        VenueFactory(site_id='101c', name=u'Venue1')
        db.session.commit()

        response = self.client.get(self.API_URL)
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
            venue.address.as_dict(include_id=False))
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
        self.assertEqual([dtime(2014, 02, 03, 12, 0, 0), dtime(2014, 02, 03, 14, 0, 0)],
                         [t.start for t in venue.times])
        self.assertTrue(venue.ad_1)
        self.assertTrue(venue.ad_2)
        self.assertTrue(venue.ad_3)
        self.assertTrue(venue.ad_4)
        self.assertTrue(venue.ad_5)
        self.assertTrue(venue.ad_6)
        self.assertTrue(venue.ad_7)
        self.assertFalse(venue.ad_8)

    def test_delete_nonexisting(self):
        self.assertObjectCount(0)
        response = self.client.delete(urljoin(self.MANAGE_API_URL, '%d/' % 5))
        self.assert404(response)
        self.FACTORY(id=4)
        response = self.client.delete(urljoin(self.MANAGE_API_URL, '%d/' % 5))
        self.assert404(response)

    def test_delete_existing(self):
        self.assertObjectCount(0)
        self.FACTORY(id=5)
        db.session.commit()
        self.assertObjectCount(1)
        self.client.delete(urljoin(self.MANAGE_API_URL, '%d/' % 5))
        self.assertObjectCount(0)

    def test_put(self):
        venue_id = 77
        self.assertObjectCount(0)
        venue = self.FACTORY(id=venue_id)
        PersonFactory(sub='112', role='artist')
        PersonFactory(sub='223', role='staff')
        EventFactory(id=8)
        db.session.commit()
        data = {
            'site_id': "*modified* 101c",
            'name': u"*modified* Gallery Happy",
            'event_id': 8,
            'picture': u'*modified* http://www.galleryhappy.com/logo.png',
            'address': {
                "street": u"*modified* 621 East Sixth Street",
                "locality": u"*modified* Austin",
                "region": u"*modified* TX",
                "postal_code": 78702,
                "country": u"*modified* US"
            },
            'twitter': '@modified_GalleryHappy',
            'email': 'modified@galleryhappy.org',
            'phone': '+1 512-555-1213',
            'category': u'*modified* Artists & Studios',
            'mediums': ["*modified* Ceramics"],
            'description': u"*modified* Fun stuff made of clay by talented people.",
            'artists': ['112'],
            'websites': [u'http://www.modified.com', u'http://modified_google.com'],
            'managers': ['223'],
            'curated': False,
            'times': ['Feb  4 12:41:00 UTC 2014', 'Feb  4 14:36:00 UTC 2014'],
            'ad_1': False,
            'ad_2': True,
            'ad_3': True,
            'ad_4': False,
            'ad_5': False,
            'ad_6': True,
            'ad_7': False,
            'ad_8': True,
        }
        self.assertNotEqual(venue.site_id, "*modified* 101c")
        self.assertNotEqual(venue.name, u"*modified* Gallery Happy")
        self.assertNotEqual(venue.event_id, 8)
        self.assertNotEqual(venue.picture, u'*modified* http://www.galleryhappy.com/logo.png')
        self.assertNotEqual({
                "street": u"*modified* 621 East Sixth Street",
                "locality": u"*modified* Austin",
                "region": u"*modified* TX",
                "postal_code": 78702,
                "country": u"*modified* US"
            },
            venue.address.as_dict(include_id=False),)
        self.assertNotEqual(venue.twitter, '@modified_GalleryHappy')
        self.assertNotEqual(venue.email, 'modified@galleryhappy.org')
        self.assertNotEqual(venue.phone, '+1 512-555-1213')
        self.assertNotEqual(venue.category, u'*modified* Artists & Studios')
        self.assertNotEqual([m.name for m in venue.mediums], ["*modified* Ceramics"])
        self.assertNotEqual(venue.description, u"*modified* Fun stuff made of clay by talented people.")
        self.assertNotEqual([a.sub for a in venue.artists], ['112'])
        self.assertNotEqual([w.url for w in venue.websites], [u'http://www.modified.com', u'http://modified_google.com'])
        self.assertNotEqual([m.sub for m in venue.managers], ['223'])
        self.assertNotEqual(venue.curated, False)
        self.assertNotEqual([t.start for t in venue.times],
                            [dtime(2014, 2, 4, 12, 41, 0), dtime(2014, 2, 4, 14, 36, 00)])
        self.assertNotEqual(venue.ad_1, False)
        self.assertNotEqual(venue.ad_2, True)
        self.assertNotEqual(venue.ad_3, True)
        self.assertNotEqual(venue.ad_4, False)
        self.assertNotEqual(venue.ad_5, False)
        self.assertNotEqual(venue.ad_6, True)
        self.assertNotEqual(venue.ad_7, False)
        self.assertNotEqual(venue.ad_8, True)

        self.client.put(urljoin(self.MANAGE_API_URL, '%d/' % venue_id),
                        data=json.dumps(data),
                        content_type='application/json')
        self.assertEqual(venue.site_id, "*modified* 101c")
        self.assertEqual(venue.name, u"*modified* Gallery Happy")
        self.assertEqual(venue.event_id, 8)
        self.assertEqual(venue.picture, u'*modified* http://www.galleryhappy.com/logo.png')
        self.assertEqual({
                             "street": u"*modified* 621 East Sixth Street",
                             "locality": u"*modified* Austin",
                             "region": u"*modified* TX",
                             "postal_code": 78702,
                             "country": u"*modified* US"
                         },
                         venue.address.as_dict(include_id=False),)
        self.assertEqual(venue.twitter, '@modified_GalleryHappy')
        self.assertEqual(venue.email, 'modified@galleryhappy.org')
        self.assertEqual(venue.phone, '+1 512-555-1213')
        self.assertEqual(venue.category, u'*modified* Artists & Studios')
        self.assertEqual([m.name for m in venue.mediums], ["*modified* Ceramics"])
        self.assertEqual(venue.description, u"*modified* Fun stuff made of clay by talented people.")
        self.assertEqual([a.sub for a in venue.artists], ['112'])
        self.assertEqual([w.url for w in venue.websites], [u'http://www.modified.com', u'http://modified_google.com'])
        self.assertEqual([m.sub for m in venue.managers], ['223'])
        self.assertEqual(venue.curated, False)
        self.assertEqual([t.start for t in venue.times],
                         [dtime(2014, 2, 4, 12, 41, 0), dtime(2014, 2, 4, 14, 36, 00)])
        self.assertEqual(venue.ad_1, False)
        self.assertEqual(venue.ad_2, True)
        self.assertEqual(venue.ad_3, True)
        self.assertEqual(venue.ad_4, False)
        self.assertEqual(venue.ad_5, False)
        self.assertEqual(venue.ad_6, True)
        self.assertEqual(venue.ad_7, False)
        self.assertEqual(venue.ad_8, True)
