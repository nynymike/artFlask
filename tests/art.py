from ..tests import TestCase
from ..tests.data.helpers import genArt
import json
class ArtTest(TestCase):

	def test_show(self):
		self._test_get_request('/api/v1/artists/')

	def test_post_art(self):
		art = genArt(self.artist_id,self.venue_id)
		respose = self._test_post_request('/api/v1/art/',data=json.dumps(art))