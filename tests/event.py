import json
from datetime import date
from urlparse import urljoin

from . import TestCase
from .factories import EventFactory

from app import db
from model import Event


class EventTestCase(TestCase):
    API_URL = '/api/v1/events/'
    MANAGE_API_URL = '/api/v1/manage/events/'
    MODEL = Event
    FACTORY = EventFactory

    def test_empty_eventllist(self):
        """
        Test empty request, empty response
        :return:
        """
        response = self.client.get(self.API_URL)
        self.assert404(response)

        response = self.client.get(urljoin(self.API_URL, 'some_event_name/'))
        self.assert404(response)

    def test_single_event(self):
        """
        Test single event
        :return:
        """
        # create an event
        EventFactory(name=u'event1')
        db.session.commit()

        response = self.client.get(self.API_URL)
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

    def test_add_event(self):
        self.assertEqual(0, self.MODEL.query.count())
        data = {
            'name': u'Happy Tour 2014',
            'start_date': 'Feb 03 2014',
            'end_date': 'Feb 05 2014',
            'description': u"This is a tour of all the artwork that you "
                           u"would want to see to make you smile",
            'picture': u'http://happytour.org/happy2014.png'
        }
        self.client.post(self.MANAGE_API_URL, data=json.dumps(data),
                         follow_redirects=True, content_type='application/json')
        self.assertEqual(1, self.MODEL.query.count())
        event = self.MODEL.query.first()
        self.assertIsNotNone(event)
        self.assertEqual(u'Happy Tour 2014', event.name)
        self.assertEqual(date(2014, 02, 03), event.start_date)
        self.assertEqual(date(2014, 02, 05), event.end_date)
        self.assertEqual(u"This is a tour of all the artwork that you "
                         u"would want to see to make you smile",
                         event.description)
        self.assertEqual(u'http://happytour.org/happy2014.png', event.picture)

    def test_deletion(self):
        self.assertObjectCount(0)
        self.FACTORY(id=5)
        db.session.commit()
        self.assertObjectCount(1)
        self.client.delete(urljoin(self.MANAGE_API_URL, '%d/' % 5))
        self.assertObjectCount(0)

