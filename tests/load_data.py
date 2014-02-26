import sys
import os
sys.path.append("%s/../"%os.getcwd())
from conf import BaseConfig
from data.helpers import genPerson,genArt,genVenue
from random import *

from pymongo import MongoClient

def main():
	client = MongoClient('localhost', 27017)
	db = client[BaseConfig.MONGO_DBNAME]
	artists = {}
	numStaff = 4
	numArtists = 250
	numVenueManagers = 2
	numVenues = 200
	numArt = 500
	# generate staff
	i=0
	while i < numStaff:
	    i = i + 1
	    d = genPerson('staff')
	    db.Person.save(d)

	# generate artists
	i=0
	while i < numArtists:
	    i = i + 1
	    d = genPerson('artist')
	    db.Person.save(d)
	    artists[d['id']] = d
	    

	# generate venues
	i=0
	while i < numVenues:
	    i = i + 1
	    artist_ids = artists.keys()
	    num_artists = randint(1,3)
	    k = 0
	    venueArtists = []
	    while k <= num_artists:
	        k = k + 1
	        artistIndex = randint(0, len(artist_ids)-1)
	        id = artist_ids[artistIndex]
	        venueArtists.append(id)
	        del artist_ids[artistIndex]
	    d = genVenue(i, venueArtists, [venueArtists[0]])
	    db.Venue.save(d)

	# generate art
	i=0
	while i < numArt:
	    i = i + 1
	    artist_ids = artists.keys()
	    random_artist = artist_ids[randint(0,(len(artist_ids)-1))]
	    d = genArt(random_artist, artists[random_artist])
	    db.ArtWork.save(d)

	event = {
	'name': 'Happy Tour 2014',
	'startDate': 'Feb  3 00:00:00 UTC 2014',
	'endDate': 'Feb  5 00:00:00 UTC 2014',
	'description': 'This is a tour of all the artwork that you would want to see to make you smile',
	'picture': 'http://aloft.gluu.org/images/happy2014.png'
	}

	db.Event.save(event)

if __name__ == '__main__':
	main()