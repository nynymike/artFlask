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

    def test_add_event(self):
        response = self.app.post('/api/v1/manage/event/', data={
             "id": "52ffa23745a8842d2e6aba6b",
             "startDate": "Feb  3 00:00:00 UTC 2014",
             "endDate": "Feb  5 00:00:00 UTC 2014",
             "description": "This is a tour of all the artwork that you would want to see to make you smile",
             "picture": "url_goes_here",
             "name": "Happy Tour 2014"
            })
        assert response.status_code==201

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

    # Test should show that the person activated the link
    # and that the status was set to Active
    def test_activate_registration(self):
        assert False


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass