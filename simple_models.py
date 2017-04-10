""" Models that are not tied to the database """


class Location:

    street_address = None
    city = None
    state = None
    zipcode = None
    latitude = None
    longitude = None

    def __str__(self):
        return '{0}, {1}, {2} {3:05d}'.format(self.street_address, self.city, self.state, self.zipcode)


class Store:

    store_id = None
    name = None
    location = None

    def __str__(self):
        return '(ID: {0}) {1} at {2}'.format(self.store_id, self.name, self.location)


class FoodItem:

    aisle = None
    category = None
    description = None
    item_id = None
    image_url = None
    name = None
