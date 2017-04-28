""" Models that are not tied to the database """


class Location:

    DB_TABLE_NAME = 'locations'

    id = None
    street_address = None
    city = None
    state = None
    zipcode = None
    latitude = None
    longitude = None
    store_id = None

    def __init__(self, street_address, city, state, zipcode, latitude=None, longitude=None, row_id=None, store_id=None):
        """ Creates a new Location object.
            :param street_address: the street address (e.g. 123 Market St) - string
            :param city: the city name (e.g. Needham) - string
            :param state: the state's abbreviation (e.g. MA) - string
            :param zipcode: the zip code of the location (e.g. 2492) - int
            :param latitude: the latitude in decimal degrees - double
            :param longitude: the longitude in decimal degrees - double
            :param store_id: the 'id' value of the corresponding store in the 'stores' table - int
        """
        self.id = row_id
        self.store_id = store_id
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return '{0}, {1}, {2} {3:05d}'.format(self.street_address, self.city, self.state, self.zipcode)


class Store:

    DB_TABLE_NAME = 'stores'

    id = None
    store_id = None
    name = None
    location = None
    items = None

    def __init__(self, store_id, name, location, row_id=None, items = []):
        self.id = row_id
        self.store_id = store_id
        self.name = name
        self.location = location
        self.items = items


    def __str__(self):
        list_of_ings = ''
        for item in self.items:
            list_of_ings += item + ' and'
        list_of_ings = list_of_ings[:-4]
        print(len(self.items   ))
        return list_of_ings #'(ID: {0}) {1} at {2}'.format(self.store_id, self.name, self.location)


class FoodItem:

    DB_TABLE_NAME = 'items'

    id = None
    aisle = None
    category = None
    description = None
    item_id = None
    image_url = None
    name = None
