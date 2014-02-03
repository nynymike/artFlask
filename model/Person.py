"""
.. currentmodule:: model.Person

Person Standard Schema
----------------------

For a list of standard person claims for OpenID Connect 1.0 see http://openid.net/specs/openid-connect-core-1_0.html#StandardClaims

Person Custom Schema
--------------------

+------------+--------------+------------------------------------------------------------------------+
| member     | type         | description                                                            |
+============+==============+========================================================================+
| twitter    | string       | Twitter handle for the person                                          |
+------------+--------------+------------------------------------------------------------------------+
| role       | string       | One or more of the following: patron, artist, staff, venueManager      |
+------------+--------------+------------------------------------------------------------------------+
| art        | List<string> | List of art_ids created by the person                                  |
+------------+--------------+------------------------------------------------------------------------+

"""

class Person():
    def __init__(self):
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
        self.art = []

    def not_empty(self, s):
        if s != "": return True
        return False

    def __str__(self):
        d = {}
        if self.not_empty(self.sub): d['sub'] = self.sub
        if self.not_empty(self.name): d['name'] = self.name
        if self.not_empty(self.given_name): d['given_name'] = self.given_name
        if self.not_empty(self.family_name): d['family_name'] = self.family_name
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
        if len(self.art): d['art'] = self.art
        return str(d)
