import os
import unittest
import artFlask

# Generate data for coverage report
from coverage import coverage
cov = coverage(branch = True, omit = ['conf.py', 'Properties.py'])
cov.start()

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
    cov.stop()
    cov.save()
    #print "\n\nCoverage Report:\n"
    #cov.report()
    #basedir = "."
    #directory = os.path.join(basedir, "tmp/coverage")
    #cov.html_report(directory)
    #print "HTML version: %s/index.html" % directory
    # cov.erase()