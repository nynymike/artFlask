import json
from urlparse import urljoin

from . import TestCase
from .factories import EventFactory
from app import db


class EventTestCase(TestCase):
    BASE_API_URL = '/api/v1/events/'

    def test_empty_eventllist(self):
        """
        Test empty request, empty response
        :return:
        """
        response = self.client.get(self.BASE_API_URL)
        self.assert404(response)

        response = self.client.get(urljoin(self.BASE_API_URL, 'some_event_name/'))
        self.assert404(response)

    def test_single_event(self):
        """
        Test single event
        :return:
        """
        # create an event
        EventFactory(name=u'event1')
        db.session.commit()

        response = self.client.get(self.BASE_API_URL)
        self.assert200(response)
        data = json.loads(response.data)
        self.assertIn('item_list', data)
        self.assertEqual(1, len(data['item_list']))
        event = data['item_list'][0]
        self.assertEqual(u'event1', event['name'])
        self.assertEqual('Mon Feb 03 2014', event['start_date'])
        self.assertEqual('Wed Feb 05 2014', event['end_date'])
        self.assertEqual(u'This is a tour of all the artwork that you '
                         u'would want to see to make you smile',
                         event['description'])
        self.assertEqual(u'http://happytour.org/happy2014.png', event['picture'])


