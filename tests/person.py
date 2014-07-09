import json
import hashlib

from . import TestCase
from factories import PersonFactory
from app import db


class ArtistTestCase(TestCase):
    def test_empty_artist_list(self):
        result = self.client.get('/api/v1/artists/')
        self.assert404(result)

    def test_artist_by_id(self):
        person = PersonFactory.create(given_name=u"Pedro")
        db.session.commit()

        result = self.client.get('/api/v1/artists/%s' % person.sub)
        self.assert200(result)
        artist_data = json.loads(result.data)
        self.assertEqual(artist_data.get('given_name'), u"Pedro")

    def test_single_artist(self):
        # just create a person
        PersonFactory.create()
        db.session.commit()
        result = self.client.get('/api/v1/artists/')
        self.assert200(result)
        data = json.loads(result.data)
        persons = data.get('item_list')
        self.assertIsNotNone(persons)
        self.assertEqual(len(persons), 1)
        result_person = persons[0]
        self.assertEqual(result_person['given_name'], u'Michael')
        self.assertEqual(result_person['family_name'], u'Schwartz')
        # self.assertEqual(result_person['name'], u'Michael Schwartz')
        self.assertEqual(result_person['email'], u'mike@gluu.org')
        self.assertEqual(result_person['phone_number'], '15125551212')
        self.assertEqual(result_person['picture'], u'http://www.gluu.org/wp-content/uploads/2012/04/mike3.png')
        self.assertDictEqual(result_person['address'], {
            u'country': u'US',
            u'region': u'TX',
            u'postal_code': 78701,
            u'street': u'621 East Sixth Street',
            u'locality': u'Austin',
        })
        self.assertEqual(result_person['role'], 'artist')
        self.assertEqual(result_person['status'], 'active')

        self.assertEqual(result_person['nickname'], 'Mike')

        self.assertListEqual(result_person['social_urls'], [
            {
                'name': 'FB',
                'url': 'https://www.facebook.com/nynymike',
            },
            {
                'name': 'LinkedIn',
                'url': 'http://www.linkedin.com/in/nynymike',
            }
        ])
        self.assertEqual(result_person['twitter'], '@nynymike')

        self.assertEqual(result_person['registration_code'], {
            hashlib.sha224('1').hexdigest(): {
                'accepted': 'Mon Feb  3 10:15:09 2014',
                'sent': 'Mon Feb  3 10:10:31 2014'
            }
        })
