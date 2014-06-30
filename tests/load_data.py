import sys
import os
import shutil
from conf import BaseConfig
from data.helpers import genPerson, genArt, genVenue
from random import *
from PIL import Image

from pymongo import MongoClient


def main():
    client = MongoClient('localhost', 27017)
    db = client[BaseConfig.MONGO_DBNAME]
    artists = {}
    numStaff = 4
    numArtists = 250
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
        artist_id = db.Person.save(d)
        artists["%s"%artist_id] = "%s"%artist_id

    # generate event
    event = {
    'name': 'Happy Tour 2014',
    'startDate': 'Feb  3 00:00:00 UTC 2014',
    'endDate': 'Feb  5 00:00:00 UTC 2014',
    'description': 'This is a tour of all the artwork that you would want to see to make you smile',
    'picture': 'http://aloft.gluu.org/images/happy2014.png'
    }
    event_id = db.Event.save(event)

    # generate Venues
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
        d = genVenue(i, venueArtists, [venueArtists[0]],event_id)
        db.Venue.save(d)

    # generate art
    i=0
    while i < numArt:
        i = i + 1
        print i
        artist_ids = artists.keys()
        random_artist = artist_ids[randint(0,(len(artist_ids)-1))]
        d = genArt(random_artist, artists[random_artist])
        art_id = db.ArtWork.save(d)
        uploadFolder = BaseConfig.UPLOAD_FOLDER
        file = "./data/images/art/0%s.jpg" % `randint(0,70)`.zfill(2)
        image=Image.open(file)
        image.save("%s/%s.png" % (uploadFolder, art_id), "PNG")
        image=Image.open(file)
        image.thumbnail((100,100), Image.ANTIALIAS)
        image.save("%s/%s_tn.png" % (uploadFolder, art_id), "PNG")
        shutil.copyfile("./data/images/qrcodes/qrcode.png", "%s/%s_qr.png" % (uploadFolder, art_id))

if __name__ == '__main__':
    main()