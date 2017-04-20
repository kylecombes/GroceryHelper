""" Models that are not tied to the database """


class Location:

    DB_TABLE_NAME = 'planner_location'

    street_address = None
    city = None
    state = None
    zipcode = None
    latitude = None
    longitude = None

    def __init__(self, street_address, city, state, zipcode, latitude=None, longitude=None):
        """ Creates a new Location object.
            :param street_address: the street address (e.g. 123 Market St) - string
            :param city: the city name (e.g. Needham) - string
            :param state: the state's abbreviation (e.g. MA) - string
            :param zipcode: the zip code of the location (e.g. 2492) - int
        """

        self.street_address = street_address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return '{0}, {1}, {2} {3:05d}'.format(self.street_address, self.city, self.state, self.zipcode)


class Store:

    DB_TABLE_NAME = 'planner_store'

    store_id = None
    name = None
    location = None
    items = None

    def __init__(self, store_id, name, location):
        self.store_id = store_id
        self.name = name
        self.location = location


    def __str__(self):
        return '(ID: {0}) {1} at {2}'.format(self.store_id, self.name, self.location)


class FoodItem:

    aisle = None
    category = None
    description = None
    item_id = None
    image_url = None
    name = None
