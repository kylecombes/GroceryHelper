"""Use this file for geo-coding related stuff"""

import json
import math
from urllib.parse import urlencode
from urllib.request import urlopen

from keys import *


class Geolocation:

    GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
    GMAPS_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json?"
    GMAPS_DIST_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
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

    @staticmethod
    def get_travel_distances(origins, destinations):
        """ Gets the driving distance between all of the origins and all of the destinations.
            :param origins the starting locations - [Location]
            :param destinations the ending locations - [Location]
            :return a len(origins) X len(destinations) matrix with the driving distances between each origin and each destination
        """
        dest_str = '|'.join((Geolocation.format_location_for_google(loc) for loc in origins))
        origin_str = '|'.join((Geolocation.format_location_for_google(loc) for loc in destinations))
        paramsurldist = Geolocation.GMAPS_DIST_BASE_URL + 'units=imperial&origins=' + origin_str + '&destinations=' + dest_str + '&key=' + KEY_DIST
        datadist = Geolocation.__get_json(paramsurldist)
        return datadist

    @staticmethod
    def get_directions(origin, stops):
        origin_str = '{street},{city},{state} {zip}'\
            .format(street=origin.street_address, city=origin.city, state=origin.state, zip=origin.zipcode)
        waypoints = ''
        for stop in stops:
            waypoints += Geolocation.format_location_for_google(stop.location) + '|'
        waypoints = waypoints[:-1]
        url = 'https://www.google.com/maps/embed/v1/directions?key=' + MAPS_API_KEY + '&origin=' + origin_str + '&destination=' + origin_str + '&waypoints=' + waypoints
        return url

    @staticmethod
    def format_location_for_google(location):
        street = location.street_address.replace(' ','+')
        city = location.city.replace(' ','+')
        return '{street},{city},{state}+{zip}'\
            .format(street=street, city=city, state=location.state, zip=location.zipcode)


class DistanceMapper:
    """ Given two locations, tells you the number of miles driving between them. """

    dists = {}

    def load_distances(self, origins, destinations):

        # Use the Google Distance Matrix API to get the driving distances between all the locations
        dists = Geolocation.get_travel_distances(origins, destinations)
        # Convert the data from JSON to dictionaries indexed by locations
        if 'error_message' in dists:
            return -1  # Likely too many origins and destinations for one API call
        rows = dists['rows']
        for i in range(len(rows)):
            cols = rows[i]['elements']
            origin = origins[i]
            for j in range(len(cols)):
                dest = destinations[j]
                if dest != origin:  # Don't store a path from a location to itself
                    dist = cols[j]['distance']['value']/1609  # Convert meters to miles
                    self.add_dist(origin, dest, dist)

    def add_dist(self, origin, destination, dist):
        """ Saves a distance calculation between two locations.
        :param origin: the originating location - Location
        :param destination: the end location - Location
        :param dist: the number of driving miles between the two locations - int
        """
        if origin not in self.dists:
            self.dists[origin] = {}
        if destination not in self.dists:
            self.dists[destination] = {}
        self.dists[origin][destination] = dist
        self.dists[destination][origin] = dist

    def get_distance(self, origin, destination):
        """ Looks up the distance between two locations.
            :param origin: the originating location - Location
            :param destination: the end location - Location
            :return the number of driving miles between the two locations - int
        """
        # Check to see if we know this distance. If not, load it first.
        if origin not in self.dists and destination not in self.dists:
            self.load_distances([origin], [destination])
        return self.dists[origin][destination]
