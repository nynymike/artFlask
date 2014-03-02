from uuid import *
from random import *
from bson import json_util
import base64, traceback
import api.venueFunctions

numStaff = 4
numArtists = 250
numVenueManagers = 2
numVenues = 200
numArt = 500

staff = {}
artists = {}
venues = {}
art = {}

artistVenueMap = {}

basePictureURL = "http://aloft.gluu.org"

def getPhone():
    return "1-512-%i%i%i-%i%i%i%i" % (randint(2,9),randint(0,9),randint(0,9),
                                    randint(0,9),randint(0,9),randint(0,9),randint(0,9))

def getBoolean():
    return randint(0,1) == True

def getTimes():
    l = ['Feb  3 12:00:00 UTC 2014', 'Feb  3 15:00:00 UTC 2014']
    i = randint(0,1)
    return [l[i]]

def getRandom(fn):
    f = open("data/%s"%fn)
    lines = f.readlines()
    f.close()
    return (lines[randint(0,len(lines) -1)]).strip()

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
    import os, os.path
    d = {
        'artist': artist_id,
        'title': getRandom('titles.txt'),
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'buyURL': 'http://ebay.com/item/%s' % base64.encodestring(str(os.urandom(8)).strip()),
        'venue': venue_id,
        'medium': getRandom('medium.txt'),
        'sold_out': getBoolean(),
        'size': '%i x %i' % (randint(10,90), randint(10,90)),
        'year': '2014',
        'alt_urls': {'Detail': 'http://www.%s/%s' % (getRandom('domains.txt'), base64.encodestring(str(os.urandom(4))).strip())}
    }
    return d

def genPerson(role=None):
    username = getRandom('usernames.txt')
    d = {
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
        d['picture'] = "%s/women/person%i.jpg" % (basePictureURL, randint(0,14))
    else:
        d['given_name'] = getRandom('boys_names.txt')
        d['picture'] = "%s/men/person%i.jpg" % (basePictureURL, randint(0,12))
    return d

def genVenue(i=0, artists=[], managers=[],event_id=""):
    username = getRandom('usernames.txt')
    street = getRandom("address.txt")
    geoCode = {}
    try:
        geoCode = api.venueFunctions.geoCode(street, "Austin", "TX", "78702")
    except:
        traceback.print_stack()
    return {
         'site_id': `i`,
         'name': getRandom("venues.txt"),
         'event_id': event_id,
         'picture': '%s/images/venues/0%s.jpg' % (basePictureURL, `randint(0,20)`.zfill(2)),
         'address': {"street": getRandom("address.txt"),
                 "city": "Austin",
                 "state": "TX",
                 "zip": "78702",
                 "country": "US"},
         'coordinates': geoCode,
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

