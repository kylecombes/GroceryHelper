

class Store:

    def __init__(self, store_id, name, address, city, state, zipcode, phone):
        """ Creates a new Store object

            :param store_id: the unique identifier of the store - string
            :param name: the user-friendly name of the store - string
            :param address: the street address of the store - string
            :param city: the city the store is in - string
            :param state: the two-letter, capital abbreviation of the state the store is in - string
            :param zipcode: the zip code of the city the store is in - int
            :param phone: the phone number of the store - string
        """
        self.store_id = store_id  # 'id' is already a built-in attribute
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone

    def merge(self, new_store):
        """ Add data from another Store object. New attribute values are added and existing ones are updated, so long as
            the new values are not None or of length 0 (for strings). I.e. blank attributes on new_store are ignored.

            :param new_store: a store to import values from - Store
        """
        if new_store.name and len(new_store.name) > 0:
            self.name = new_store.name
        if new_store.address and len(new_store.address) > 0:
            self.address = new_store.address
        if new_store.city and len(new_store.city) > 0:
            self.city = new_store.city
        if new_store.state and len(new_store.state) > 0:
            self.state = new_store.state
        if new_store.zip and new_store.zip > 0:
            self.zipcode = new_store.zip
        if new_store.phone and new_store.phone > 0:
            self.phone = new_store.phone

    def __str__(self):
        return '(ID: {0}) {1} at {2}, {3}, {4} {5:05d}'.format(self.store_id, self.name, self.address, self.city, self.state, self.zipcode)
