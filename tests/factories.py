import factory
from factory.alchemy import SQLAlchemyModelFactory
import model
import hashlib
from tests import db
import datetime


class RegistrationCodeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.RegistrationCode
        sqlalchemy_session = db.session

    sent = datetime.datetime(2014, 2, 3, 10, 10, 31)
    accepted = datetime.datetime(2014, 2, 3, 10, 15, 9)


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


class ArtFactory(SQLAlchemyModelFactory):
    class Meta:
        model = model.Artwork
        sqlalchemy_session = db.session

