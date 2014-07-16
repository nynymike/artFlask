import json
from urlparse import urljoin
import hashlib

from . import TestCase
from factories import PersonFactory
from app import db
from model import Person


class ArtistTestCase(TestCase):
    MODEL = Person
    FACTORY = PersonFactory
    MANAGE_API_URL = '/api/v1/manage/persons/'

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

    def test_deletion(self):
        self.assertObjectCount(0)
        self.FACTORY(sub='5')
        db.session.commit()
        self.assertObjectCount(1)
        self.client.delete(urljoin(self.MANAGE_API_URL, '%s/' % '5'))
        self.assertObjectCount(0)

    def test_put(self):
        self.assertObjectCount(0)
        person_sub = '1121'
        person = self.FACTORY(sub=person_sub)
        db.session.commit()
        self.assertObjectCount(1)
        data = {
            'given_name': u'*modified* Michael',
            'family_name': u'*modified* Schwartz',
            'email': u'*modified.mike@gluu.org',
            'phone_number': '1-512-555-1213',
            'picture': u'http://www.modified.org/1.png',
            "address": {
                "street": u"*modified* 621 East Sixth Street",
                "locality": u"*modified* Austin",
                "region": u"*modified* TX",
                "postal_code": 78702,
                "country": u"*modified* US"
            },
            'nickname': u'*modified* Mike',
            'social_urls': {
                'FB': u'https://www.facebook.com/modified_nynymike',
                'LinkedIn': u'http://www.linkedin.com/in/modified_nynymike'
            },
            'role': 'staff',  # TODO(analytic): shouldn't be changeable
            'twitter': '@modified_nynymike',
            'preferred_contact': 'Voice',
            'status': 'inactive',
            'registration_code': {
                'e086acd2-2d0f-440b-bbd0-dbde47301b01': {
                    'sent': 'Feb 04 10:10:31 2014',
                    'accepted': 'Feb 04 10:15:09 2014'
                }
            }
        }

        self.assertNotEqual(person.given_name, u'*modified* Michael')
        self.assertNotEqual(person.family_name, u'*modified* Schwartz')
        self.assertNotEqual(person.email, u'*modified.mike@gluu.org')
        self.assertNotEqual(person.phone_number, '1-512-555-1213')
        self.assertNotEqual(person.picture, u'http://www.modified.org/1.png')
        self.assertNotEqual({
                "street": u"*modified* 621 East Sixth Street",
                "locality": u"*modified* Austin",
                "region": u"*modified* TX",
                "postal_code": 78702,
                "country": "*modified* US"
            },
            person.address)
        self.assertNotEqual(person.nickname, u'*modified* Mike')
        self.assertNotEqual({u.name: u.url for u in person.social_urls}, {
               'FB': u'https://www.facebook.com/modified_nynymike',
               'LinkedIn': u'http://www.linkedin.com/in/modified_nynymike'
           })
        self.assertNotEqual(person.role, '*modified* artist')  # TODO(analytic): shouldn't be changeable
        self.assertNotEqual(person.twitter, '@modified_nynymike')
        self.assertNotEqual(person.preferred_contact, 'Voice')
        self.assertNotEqual(person.status, 'inactive')
        self.assertNotEqual(person.registration_code, {
            'e086acd2-2d0f-440b-bbd0-dbde47301b01': {
                'sent': 'Feb 04 10:10:31 2014',
                'accepted': 'Feb 04 10:15:09 2014'
            }})

        # remember reg code before update
        reg_code = person.registration_code.as_dict()

        response = self.client.put(urljoin(self.MANAGE_API_URL, '%s/' % person_sub),
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assert200(response)

        self.assertEqual(person.given_name, u'*modified* Michael')
        self.assertEqual(person.family_name, u'*modified* Schwartz')
        self.assertEqual(person.email, u'*modified.mike@gluu.org')
        self.assertEqual(person.phone_number, '1-512-555-1213')
        self.assertEqual(person.picture, u'http://www.modified.org/1.png')
        self.assertDictEqual({
                "street": u"*modified* 621 East Sixth Street",
                "locality": u"*modified* Austin",
                "region": u"*modified* TX",
                "postal_code": 78702,
                "country": "*modified* US"
            },
            person.address.as_dict())
        self.assertEqual(person.nickname, u'*modified* Mike')
        self.assertEqual({u.name: u.url for u in person.social_urls}, {
            'FB': u'https://www.facebook.com/modified_nynymike',
            'LinkedIn': u'http://www.linkedin.com/in/modified_nynymike'
        })
        self.assertEqual(person.role, 'artist')  # TODO(analytic): shouldn't be changeable
        self.assertEqual(person.twitter, '@modified_nynymike')
        self.assertEqual(person.preferred_contact, 'Voice')
        self.assertEqual(person.status, 'inactive')

        # TODO(analytic): interface for changing reg code
        # verify registration code didn't change
        self.assertEqual(person.registration_code.as_dict(), reg_code)
