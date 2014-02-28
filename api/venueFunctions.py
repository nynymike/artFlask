# http://www.mapquestapi.com/geocoding/
# Example GET looking up one request:
# http://www.mapquestapi.com/geocoding/v1/address?&key=YOUR-KEY-HERE&location=1555 Blake St,Denver,CO,80202
from flask import current_app

# Returns dictionary for example: {u'lat': 30.26068, u'lng': -97.7319}
# and response code 0 for success, and 1 if error parsing results, 2 for other errors
def geoCode(street, city, state, zip):
    try:
        import urllib, urllib2, json
        apikey = current_app.config['MAPQUEST_API_KEY']
        address = urllib.quote('%s,%s,%s,%s' % (street, city, state, zip))
        url = 'http://www.mapquestapi.com/geocoding/v1/address?&key=%s&location=%s' % (apikey, address)
        response = urllib2.urlopen(url).read()
        try:
            d = json.loads(response)
            coords = d['results'][0]['locations'][0]['latLng']
            return coords,0
        except Exception, e:
            return "%s+\nResponse:\n%s" % (str(e), response),1
    except Exception, e:
        return str(e),2

def test():
    import urllib, urllib2, json
    apikey = '<enter mapquest api key here>'
    address = urllib.quote("621 East Sixth Street,Austin,TX,78702")
    url = 'http://www.mapquestapi.com/geocoding/v1/address?&key=%s&location=%s' % (apikey, address)
    print url
    response = urllib2.urlopen(url).read()
    d = json.loads(response)
    coords = d['results'][0]['locations'][0]['latLng']
    print coords

if __name__ == '__main__':
    test()
