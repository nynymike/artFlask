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
        rv = self.app.get("/")
        assert 'Welcome to the artFlask API Server' in rv.data

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass