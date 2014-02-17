import random, uuid
from random import *

numVenues = 10
numArtists = 13
numArt = 10

def getRandom(fn):
    f = open(fn)
    lines = f.readlines()
    f.close()
    return (lines[randint(0,len(lines -1))])

venueTemplate="""{'id': '%(id)s',
'site_id': '%(site-id)s',
'name': '%(venue-name)s',
'event_id': '52ffa23745a8842d2e6aba6a',
'picture': '%(logoURI)s'
'address': '%(address)s'
'coordinates': ['40.446195', '-79.982195'],
'twitter': '%(twitter)s',
'mail':'%(email)s',
'phone':'+1 512-%(three)s-%(four)s',
'category':'Artists & Studios',
'medium':'%(mediums)s',
'description':'%(description)s',
'artists': ['%(artist-id)'],
'websites': ['%(websiteURI)s'],
'managers': ['%(manager-id)s'],
'ad_1': true,
'ad_2': true,
'ad_3': true,
'ad_4': true,
'ad_5': true,
'ad_6': true,
'ad_7': true,
'ad_8': false
}
"""

# some may have a series...
# some may have a parent work
# some may have alt_urls
artTemplate="""{'id': '%(id)s',
'artist': '%(artist)s',
'title': '%(title)s',
'description': '%(Descirption)s',
'picture': '%(pictureURI)s/picture',
'thumbnail': '%(pictureURI)s/thumbnmail',
'buyURL': '%(buyURI)s',
'venue': '%(venueID)s',
'medium': ''%(medium)s',
'sold_out': 'false'
'size': '24"x34"',
'year': '2014'
}
"""

personTemplate="""{ 'id': '%(id)s',
  'sub': '%(givenName)s@%(domain)s',
  'given_name': '%(givenName)s',
  'family_name': '%(family_name)s',
  'name': '%(givenName)s %(family_name)s',
  'email': '%(givenName)s@%(domain)s',
  'phone_number': '1-512-%(three)s-%(four)%',
  'picture': '%(pictureURI)s',
  'address': '%(address)s',
  'locality': '%(city)s',
  'region': '%(state)s',
  'postal_code': '%(zip)',
  'social_urls': '%(socialURIs)s'
  'role': 'artist',
  'twitter': '%(twitter)s',
  'preferred_contact': 'Email',
  'status': 'active'}
"""

i = 0
venue_list = []
used_site_ids = []
siteID = ''
while i < numVenues:
    i = i + 1
    gotID = False
    username = getRandom("usernames.txt")
    domain = getRandom("domains.txt")
    while not gotID: siteID = randint(1, 120)
    d = {'id': uuid.uuid4(),
     'site-id': siteID,
     'venue-name': getRandom("venues.txt"),
     'logoURI':'http://aloft.gluu.org/images/venues/00%i.jpg' % randint(0,9),
     'address': getRandom("address.txt"),
     'twitter':'@%s'%  username,
     'email':'%s@%s' % (username, domain),
     'three':'%i%i%i' % (randint(0,9),randint(0,9),randint(0,9)),
     'four':'%i%i%i%i' % (randint(0,9),randint(0,9),randint(0,9),randint(0,9)),
     'mediums,': getRandom("medium.txt"),
     'description':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
     'artist-id':'',
     'manager-id':'',
     'websiteURI':'http://www.%s.org' % username
    }
    venue_list.append(venueTemplate % d)

pd = {}

at = {}

