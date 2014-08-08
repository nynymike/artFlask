from . import TestCase

from model import Person
from .factories import PersonFactory


class StaffTestCase(TestCase):
    API_URL = '/api/v1/staff/'
    MODEL = Person
    FACTORY = PersonFactory

    def test_empty(self):
        response = self.client.get(self.API_URL)
        self.assert404(response)
        self.FACTORY()
