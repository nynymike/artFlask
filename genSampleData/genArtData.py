from uuid import *
from random import *
from bson import json_util

numStaff = 4
numArtists = 250
numVenueManagers = 2
numVenues = 200
numArt = 500

staff = {}
artists = {}
venueManagers = {}
venues = {}
art = {}

artistVenueMap = {}

basePictureURL = "http://aloft.gluu.org/"

def getPhone():
    three = '%i%i%i' % (randint(0,9),randint(0,9),randint(0,9)),
    four = '%i%i%i%i' % (randint(0,9),randint(0,9),randint(0,9),randint(0,9)),
    return '1-512-%s-%s' % (three, four)

def getBoolean():
    return randint(0,1)

def getTimes():
    l = []
    if randint(0,100)>95: l.append('Feb  3 12:00:00 UTC 2014')
    if randint(0,100)>95: l.append('Feb  3 15:00:00 UTC 2014')
    return l

def getRandom(fn):
    f = open(fn)
    lines = f.readlines()
    f.close()
    return (lines[randint(0,len(lines -1))])


def printJson(d):
    ids = d.keys()
    for id in ids:
        print json_util.dumps(d[id])

event = {
    'id': 'happy2014',
    'name': 'Happy Tour 2014',
    'startDate': 'Feb  3 00:00:00 UTC 2014',
    'endDate': 'Feb  5 00:00:00 UTC 2014',
    'description': 'This is a tour of all the artwork that you would want to see to make you smile',
    'picture': 'http://aloft.gluu.org/images/happy2014.png'
}

def genArt(artist_id, venue_id):
    id = uuid4()
    d = {
        'id': id,
        'artist': artist_id,
        'title': getRandom('title.txt'),
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'buyURL': 'http://ebay.com/item/%s' % uuid4()[:8],
        'venue': venue_id,
        'medium': getRandom('medium.txt'),
        'sold_out': getBoolean(),
        'size': '%i x %i' % (randint(10,90), randint(10,90)),
        'year': '2014',
        'alt_urls': {'Detail': 'http://www.%s/%s' % (getRandom('domains.txt'), uuid4()[3:9])}
    }
    if randint(0,10)>9: d['parent'] = uuid4()
    elif randint(0,10)>9: d['series'] = [uuid4(), uuid4(), uuid4()]
    return d

def genPerson(role=None):
    username = getRandom('usernames.txt')
    d = {
        'id': uuid4(),
        'sub': username,
        'family_name': getRandom('family_names.txt'),
        'phone_number': getPhone(),
        'email' : '%s@gmail.com' % username,
        'twitter': '@%s' % username,
        'status': 'active',
        'address': {"street_address": getRandom("address.txt"),
                    "locality": "Austin",
                    "region": "TX",
                    "postal_code": "78702",
                    "country": "US"}
        }
    if role: d['role'] = [role]
    if randint(0,1)==0: d['preferred_contact'] = 'email'
    elif randint(0,1)==0: d['preferred_contact'] = 'phone'
    else: d['preferred_contact'] = 'facebook'
    if randint(0,1)==0:
        d['given_name'] = getRandom('girls_names.txt')
        d['picture'] = "%s/men/person%i.jpg" % (basePictureURL, randint(0,9))
    else:
        d['given_name'] = getRandom('boys_names.txt')
        d['picture'] = "%s/men/person%i.jpg" % (basePictureURL, randint(0,9))
    return d

def genVenue(i=0, artists=[], managers=[]):
    username = getRandom('usernames.txt'),
    return {
        'id': uuid4(),
         'site-id': `i`,
         'name': getRandom("venues.txt"),
         'event_id': event['id'],
         'logoURI':'http://aloft.gluu.org/images/venues/00%i.jpg' % randint(0,9),
         'address': {"street_address": getRandom("address.txt"),
                 "locality": "Austin",
                 "region": "TX",
                 "postal_code": "78702",
                 "country": "US"},
         'twitter':'@%s' % username,
         'mail':'%s@gmail.com' % username,
         'phone': getPhone(),
         'category': 'studio',
         'mediums':[getRandom("medium.txt"), getRandom("medium.txt")],
         'description':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
         'artists': artists,
         'websites': ['http://www.%s' % getRandom('domains.txt'), 'http://www.%s' % getRandom('domains.txt')],
         'managers': managers,
         'curated': getBoolean(),
         'times': getTimes(),
         'ad_1': getBoolean(),
         'ad_2': getBoolean(),
         'ad_3': getBoolean(),
         'ad_4': getBoolean(),
         'ad_5': getBoolean(),
         'ad_6': getBoolean(),
         'ad_7': getBoolean(),
         'ad_8': getBoolean()
    }

# generate staff
i=0
while i <= numStaff:
    i = i + 1
    d = genPerson('staff')
    staff[d['id']] = d

# generate venue managers
i=0
while i <= numVenueManagers:
    i = i + 1
    d = genPerson()
    venueManagers[d['id']] = d

# generate artists
i=0
while i <= numArtists:
    i = i + 1
    d = genPerson('artist')
    artists[d['id']] = d

# generate venues
i=0
while i <= numVenues:
    i = i + 1
    artist_ids = artists.keys()
    num_artists = randint(1,3)
    k = 0
    venueArtists = []
    while k <= num_artists:
        artistIndex = randint(0, len(artist_ids))
        id = artist_ids[artistIndex]
        if id in venueArtists.keys():
            continue
        k = k + 1
        del artist_ids[artistIndex]
    d = genVenue(i, venueArtists, [venueArtists[0]])
    venues[d['id']] = d
    # Create the index of used artists
    for item in artist_ids:
        venueArtists[item] = d['id']

# generate art
i=0
while i <= numArt:
    i = i + 1
    artist_ids = venueArtists.keys()
    random_artist = artist_ids[0,len(artist_ids)-1]
    d = genArt(random_artist, venueArtists[random_artist])
    art[d['id']] = d

print json_util.dumps(event)

printJson(staff)
printJson(artists)
printJson(venueManagers)
printJson(venues)
printJson(art)

