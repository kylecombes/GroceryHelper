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
