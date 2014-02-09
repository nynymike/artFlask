"""
.. currentmodule:: model.Person

Person Standard Schema
----------------------

For a list of standard person claims for OpenID Connect 1.0 see http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims

Person Custom Schema
--------------------


+-------------------+--------------+------------------------------------------------------------------------+
| member            | type         | description                                                            |
+===================+==============+========================================================================+
| id                | string       | unique artFlask identifier                                             |
+-------------------+--------------+------------------------------------------------------------------------+
| twitter           | string       | Twitter handle for the person                                          |
+-------------------+--------------+------------------------------------------------------------------------+
| role              | string       | One or more of the following: patron, artist, staff                    |
+-------------------+--------------+------------------------------------------------------------------------+
| social_urls       | string       | Dictionary of websites given in the format {'display-name':'url'}      |
+-------------------+--------------+------------------------------------------------------------------------+
| preferred_contact | string       | Field to help the person specify how they want to be contacted         |
+-------------------+--------------+------------------------------------------------------------------------+

Person Entity JSON sample:
--------------------------

.. code-block:: javascript

   { 'id': '6b4f3db7-95dd-4ca1-a63b-abd48b1fc0f8',
     'sub': 'nynymike@gmail.com',
     'given_name': 'Michael',
     'family_name': 'Schwartz',
     'name': 'Michael Schwartz',
     'email': 'mike@gluu.org',
     'phone_number': '1-512-555-1212',
     'picture': 'http://www.gluu.org/wp-content/uploads/2012/04/mike3.png',
     "address": {"street_address": "621 East Sixth Street",
     "locality": "Austin",
     "region": "TX",
     "postal_code": "78701",
     "country": "US"},
     'nickname': 'Mike',
     'social_urls': {'FB': 'https://www.facebook.com/nynymike',
                    'LinkedIn', 'http://www.linkedin.com/in/nynymike'},
     'role': 'artist',
     'twitter': '@nynymike',
     'preferred_contact': 'Email'

"""

class Person():
    def __init__(self):
        self.id = ""
        self.sub = ""
        self.name = ""
        self.given_name = ""
        self.family_name = ""
        self.middle_name = ""
        self.nickname = ""
        self.preferred_username = ""
        self.profile = ""
        self.picture = ""
        self.website = ""
        self.email = ""
        self.email_verified = ""
        self.gender = ""
        self.birthdate = ""
        self.zoneinfo = ""
        self.locale = ""
        self.phone_number = ""
        self.phone_number_verified = ""
        self.address = ""
        self.updated_at = ""

        # Custom claims
        self.twitter = ""
        self.role = ""
        self.social_urls = {}
        self.preferred_contact = ''

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        if self.not_empty(self.id): d['id'] = self.id
        if self.not_empty(self.sub): d['sub'] = self.sub
        if self.not_empty(self.name): d['name'] = self.name
        if self.not_empty(self.given_name): d['given_name'] = self.given_name
        if self.not_empty(self.family_name): d['family_name'] = self.family_name
        if self.not_empty(self.middle_name): d['middle_name'] = self.middle_name
        if self.not_empty(self.nickname): d['nickname'] = self.nickname
        if self.not_empty(self.preferred_username): d['preferred_username'] = self.preferred_username
        if self.not_empty(self.profile): d['profile'] = self.profile
        if self.not_empty(self.picture): d['picture'] = self.picture
        if self.not_empty(self.website): d['website'] = self.website
        if self.not_empty(self.email): d['email'] = self.email
        if self.not_empty(self.email_verified): d['email_verified'] = self.email_verified
        if self.not_empty(self.gender): d['gender'] = self.gender
        if self.not_empty(self.birthdate): d['birthdate'] = self.birthdate
        if self.not_empty(self.zoneinfo): d['zoneinfo'] = self.zoneinfo
        if self.not_empty(self.locale): d['locale'] = self.locale
        if self.not_empty(self.phone_number): d['phone_number'] = self.phone_number
        if self.not_empty(self.phone_number_verified): d['phone_number_verified'] = self.phone_number_verified
        if self.not_empty(self.address): d['address'] = self.address
        if self.not_empty(self.updated_at): d['updated_at'] = self.updated_at
        if self.not_empty(self.updated_at): d['twitter'] = self.twitter
        if self.not_empty(self.updated_at): d['role'] = self.role
        if len(self.social_urls): d['social_urls'] = self.social_urls
        if self.not_empty(self.preferred_contact): d['preferred_contact'] = self.preferred_contact
        return str(d)
