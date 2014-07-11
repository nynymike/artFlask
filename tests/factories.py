import factory
from factory.alchemy import SQLAlchemyModelFactory
import model
import hashlib
from tests import db
from datetime import datetime as dtime, date


class RegistrationCodeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.RegistrationCode
        sqlalchemy_session = db.session

    sent = dtime(2014, 2, 3, 10, 10, 31)
    accepted = dtime(2014, 2, 3, 10, 15, 9)


class WebsiteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Website
        sqlalchemy_session = db.session

    name = "Google"
    url = "http://google.com"


class AddressFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Address
        sqlalchemy_session = db.session

    # id = factory.Sequence(lambda n: n)
    country = u'US'
    region = u'TX'
    postal_code = '78701'
    street = u'621 East Sixth Street'
    locality = u'Austin'


class PersonFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Person
        sqlalchemy_session = db.session

    sub = factory.Sequence(lambda n: hashlib.sha224(str(n)).hexdigest())
    given_name = u'Michael'
    family_name = u'Schwartz'
    name = factory.LazyAttribute(lambda obj: '%s %s' % (obj.given_name, obj.family_name))
    email = u'mike@gluu.org'
    phone_number = '15125551212'
    picture = u'http://www.gluu.org/wp-content/uploads/2012/04/mike3.png'
    address = factory.SubFactory(AddressFactory)

    role = 'artist'
    status = 'active'

    nickname = u'Mike'

    social_urls = []

    @factory.post_generation
    def set_social_urls(self, create, extracted, **kwargs):
        if not self.social_urls:
            self.social_urls.append(WebsiteFactory(name='FB', url='https://www.facebook.com/nynymike'))
            self.social_urls.append(WebsiteFactory(name='LinkedIn', url='http://www.linkedin.com/in/nynymike'))

    twitter = '@nynymike'
    preferred_contact = 'Email'
    registration_code = factory.SubFactory(RegistrationCodeFactory)


class EventFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Event
        sqlalchemy_session = db.session

    name = u'Happy Tour 2014'

    start_date = date(2014, 2, 3)
    end_date = date(2014, 2, 5)
    # startDate = 'Feb  3 00:00:00 UTC 2014'
    # endDate = 'Feb  5 00:00:00 UTC 2014'
    description = u'This is a tour of all the artwork that you would want to see to make you smile'
    picture = u'http://happytour.org/happy2014.png'


class MediumFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Medium
        sqlalchemy_session = db.session

    name = factory.Iterator((u'Ceramics', u'Painting'), cycle=True)


class VenueLimitedTimeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.VenueLimitedTime
        sqlalchemy_session = db.session

    start = dtime(2014, 2, 3, 0, 0, 0)
    # venue_id


class VenueFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Venue
        sqlalchemy_session = db.session

    # 'id': 'd471b627-f7f3-4872-96e2-2af4d813673f'
    site_id = factory.Sequence(lambda n: '%dc' % n)
    name = u'Gallery Happy'
    event = factory.SubFactory(EventFactory)
    picture = u'http://www.galleryhappy.com/logo.png'
    address = factory.SubFactory(AddressFactory)
    # 100 Cesar Chavez\\nAustin, TX 78702'
    latitude = 40.446195
    longitude = -79.982195
    # coordinates = ['40.446195', '-79.982195']
    twitter = '@GalleryHappy'
    email = 'info@galleryhappy.org'
    phone = '+1 512-555-1212'
    category = u'Artists & Studios'

    mediums = []

    @factory.post_generation
    def set_mediums(self, create, extracted, **kwargs):
        if not self.mediums:
            self.mediums = model.Medium.query.limit(2).all()
            required = 2
            existing = len(self.mediums)
            if existing < required:
                new_mediums = MediumFactory.create_batch(required - existing)
                self.mediums += new_mediums


    description = u'Fun stuff made of clay by talented people.'

    artists = []

    @factory.post_generation
    def set_artists(self, create, extracted, **kwargs):
        if not self.artists:
            self.artists.append(PersonFactory())

    websites = []

    @factory.post_generation
    def set_websites(self, create, extracted, **kwargs):
        if not self.websites:
            self.websites.append(
                WebsiteFactory(name='venue',
                               url='http://www.venue.com'))

    managers = []

    @factory.post_generation
    def set_managers(self, create, extracted, **kwargs):
        if not self.managers:
            self.managers.append(PersonFactory(role='staff'))
    # managers = ['c3491f70-8c92-11e3-a91c-3c970e1b8563']
    curated = True

    times = []

    @factory.post_generation
    def set_times(self, create, extracted, **kwargs):
        if not self.times:
            for t in (dtime(2014, 2, 3, 12, 0, 0), dtime(2014, 2, 3, 14, 0, 0)):
                self.times.append(
                    VenueLimitedTimeFactory(start=t, venue_id=self.id))
    # times = ['Feb  3 12:00:00 UTC 2014', 'Feb  3 14:00:00 UTC 2014']
    ad_1 = True
    ad_2 = False
    ad_3 = False
    ad_4 = True
    ad_5 = True
    ad_6 = False
    ad_7 = True
    ad_8 = False


class ArtworkFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Artwork
        sqlalchemy_session = db.session

    # id = '1d5bfb0f-8c4b-11e3-b767-3c970e1b8563'
    artist = factory.SubFactory(PersonFactory)
    title = u'Austin Sunrise'
    description = u'Third in a series of 90 painting of the beautiful Austin skyline'
    buy_url = u'http://auction.com/item/3432840932'
    venue = factory.SubFactory(VenueFactory)
    medium = 'Painting'
    sold_out = False
    series = []

    @factory.post_generation
    # @factory.post_generation(extract_prefix='related')
    def set_series(self, create, extracted, **kwargs):
        if not self.series:
            if extracted:
                self.series += extracted

    parent_work = None

    @factory.post_generation
    def set_parent(self, create, extracted, **kwargs):
        if not self.parent_work:
            if extracted:
                self.parent_work = extracted

    height = 24
    width = 34
    year = '2014'

    alt_urls = []

    @factory.post_generation
    def set_urls(self, create, extracted, **kwargs):
        if not self.alt_urls:
            for k, v in (('Detail', 'http://goo.gl/23A3fi'), ('Back', 'http://goo.gl/xc3wyo')):
                self.alt_urls.append(WebsiteFactory(name=k, url=v))

