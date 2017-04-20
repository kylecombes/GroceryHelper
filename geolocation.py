"""Use this file for geo-coding related stuff"""

import json
import math
from pprint import pprint
#from urllib.parse import urlencode
#from urllib.request import urlopen

from keys import *


class Geolocation:

    GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
    GMAPS_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json?"
    MILES_PER_DEGREE_LAT_LONG = 69

    @staticmethod
    def load_lat_long_for_location(location):
        lat_long = Geolocation.__get_lat_long(location.__str__())
        location.latitude = lat_long[0]
        location.longitude = lat_long[1]
        return lat_long

    @staticmethod
    def __get_json(url):
        """
        formats a url to take an address from the user and properly formats URL
        for a JSON web API request, return
        a Python JSON object containing the response to that request.
        """
        f = urlopen(url)
        response_text = f.read()
        response_data = str(response_text, "utf-8")
        response_data = json.loads(response_data)
        return response_data

    @staticmethod
    def __get_lat_long(place_name):
        """
        Given a place name or address, return a (latitude, longitude) tuple
        with the coordinates of the given place.

        See https://developers.google.com/maps/documentation/geocoding/
        for Google Maps Geocode API URL formatting requirements.
        """

        params_url = urlencode({'address':place_name, 'key':KEY_GEO})
        url = Geolocation.GMAPS_BASE_URL + params_url
        first_result = Geolocation.__get_json(url)['results'][0]
        return first_result['geometry']['location']['lat'], first_result['geometry']['location']['lng']

    @staticmethod
    def get_euclidean_dist(loc1, loc2):
        """ Gets the Euclidean distance (as the crow flies, in miles) between two locations.
            :param loc1 the first location - Location
            :param loc2 the second location - Location
            :return the number of miles between the two points
        """
        if not loc1.latitude:
            Geolocation.load_lat_long_for_location(loc1)
        if not loc2.latitude:
            Geolocation.load_lat_long_for_location(loc2)
        # Math from https://gis.stackexchange.com/questions/142326/calculating-longitude-length-in-miles
        delta_lat_mi = (loc2.latitude - loc1.latitude)*Geolocation.MILES_PER_DEGREE_LAT_LONG
        delta_long_mi = (loc2.longitude - loc1.longitude)*math.cos(loc1.latitude)*Geolocation.MILES_PER_DEGREE_LAT_LONG
        return math.sqrt(math.pow(delta_lat_mi, 2) + math.pow(delta_long_mi, 2))

    # TODO Get this working
    @staticmethod
    def get_travel_distance(origin, destination):
        """ Gets the driving distance between two locations.
            :param origin the first location - Location
            :param destination the second location - Location
            :return the number of miles that must be traveled to go from loc1 to loc2
        """
        origin = get_addr(get_lat_lon(origin))
        destination = get_addr(get_lat_lon(destination))
        paramsurldist = GMAPS_BASE_URL_DIST + '?units=imperial' + 'origins=' + origin + 'destinations=' + destination + '&key=' + key_dist
        datadist = get_json(paramsurldist)
        pprint(datadist)


    def get_directions(origin, destination):

        pass


    @staticmethod
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


get_travel_distance('Fenway Park','1000 Olin Way, Needham, MA 02492')
