"""

"""

from urllib.request import urlopen
from urllib.parse import urlencode
import json
from pprint import pprint
from keys import *
url = "https://maps.googleapis.com/maps/api/geocode/json?address=Fenway%20Park"


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GMAPS_BASE_URL_DIST = "https://maps.googleapis.com/maps/api/distancematrix/json"
GMAPS_BASE_URL_DIRECT = ""


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    f = urlopen(url)
    response_text = f.read()
    response_data = str(response_text, "utf-8")
    #bad_index = response_data.rfind("{")
    #response_data = response_data[0:bad_index]
    response_data = json.loads(response_data)
    #return(response_data["results"][0]["geometry"]["location"])
    return response_data
    pprint(response_data)


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """

    params = urlencode({'address':place_name, 'key':key_geo})
    #print(params)
    paramsurl = GMAPS_BASE_URL + '?' + params
    data = get_json(paramsurl)
    #pprint(data)
    #print(data['geometry']['location']['lat'], data['geometry']['location']['lng'])
    print('hgooooohg')
    return data['geometry']['location']['lat'], data['geometry']['location']['lng']

def get_addr(latitude, longitude):
    """

    """
    params1 = urlencode({'lat':latitude,'lng':longitude})
    lat = str(latitude)
    lng = str(longitude)
    #print(lat)
    paramsaddr = 'latlng' + '=' + lat + ',' + lng
    #print('goooopoooo')
    paramsurladdr = GMAPS_BASE_URL + '?' + paramsaddr + '&key=' + key_geo
    #print(paramsurladdr)
    dataaddr = get_json(paramsurladdr)
    #pprint(dataaddr)
    #print('wooooooooooooooooooo')
    #something with getting the address is wierd
    addr = (dataaddr['formatted_address'])

    #print(addr)
    return addr



def get_dist(origins,destinations):
    origin = get_addr(get_lat_lon(origins))
    #will return
    destination = get_addr(get_lat_lon(destinations))
    paramsurldist = GMAPS_BASE_URL_DIST + '?units=imperial' + 'origins=' + origin + 'destinations=' + destination + '&key=' + key_dist
    datadist = get_json(paramsurldist)
    pprint(datadist)

def get_directions():

    pass


print(get_json(url))
#print(get_lat_long('Fenway Park'))
#print(get_addr(42.3466764, -71.0972178))
#print(get_dist())
