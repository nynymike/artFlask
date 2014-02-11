import os
import unittest
import artFlask

class artFlaskTestCase(unittest.TestCase):

    def setUp(self):
        # create test mongdb
        artFlask.app.config['TESTING'] = True
        self.app = artFlask.app.test_client()

    def tearDown(self):
        # Remove mondb
        pass

    # testing functions

    def test_index(self):
        response = self.app.get("/")
        assert 'Welcome to the artFlask API Server' in response.data
        assert response.status_code == 200

    def test_register(self):
        response = self.app.post('/api/v1/register', data={
            'name':"Foo Bar",
            'given_name': "Foo",
            'family_name': "Bar",
            'middle_name': "A.",
            'nickname': "Foo-y",
            'picture': "http://vlt.me/foobar",
            'website': "http://foo.net",
            'email': "foo@bar.net",
            'gender': "M",
            'birthdate': "06-06-60",
            'phone_number': "512-555-1212",
            'address': "66 Sixth Street",
            'twitter': "@foobar",
            'social_urls': "{'facebook':'http://facebook.com/foobar'}",
            'preferred_contact': 'email'}, follow_redirects=True)
        assert response.status_code == 200

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass