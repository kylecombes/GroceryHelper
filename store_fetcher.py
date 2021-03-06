from models import Location, Store
from supermarket_api_base import SupermarketAPIBase
import threading
import requests
import untangle


class StoreFetcher(SupermarketAPIBase):

    REQUEST_NAME = 'StoresByZip'

    def __init__(self, api_key):
        super().__init__(api_key)

    def fetch_all_stores_in_zip(self, zipcode):
        """ Fetches all of the stores for a given zip code

            :param zipcode: the zip code - int
            :returns a list of Stores found - list<Store>
        """
        # Build URL to make API call
        url = self.build_url(self.REQUEST_NAME, ZipCode=zipcode)
        # Request data from server (XML)
        xml_str = requests.get(url, headers=self.HEADERS).text
        # Parse XML into an XML object
        xml = untangle.parse(xml_str)

        stores = list()

        try:
            # Create a Store object for each XML element and add it to the list
            for elem in xml.ArrayOfStore.Store:
                store_id = elem.StoreId.cdata
                name = elem.Storename.cdata.strip()
                address = elem.Address.cdata.strip()
                city = elem.City.cdata.strip()
                state = elem.State.cdata.strip()
                zip_str = elem.Zip.cdata.strip()[:5]
                zipcode = int(zip_str) if len(zip_str) > 0 else None
                # phone = elem.Phone.cdata.strip()
                loc = Location(address, city, state, zipcode)
                store = Store(store_id, name, loc)
                stores.append(store)
        except IndexError:
            pass

        return stores


class StoresDS:

    def __init__(self):
        self.stores_dict = {}
        self.lock = threading.Lock()

    def add_store(self, store):
        """ Adds a store if it is new, or updates a store if it already exists

            :param store: the store to add - Store
        """
        # Acquire a lock on this object so other threads can't modify it
        # (could be unnecessary given dictionaries are thread-safe).
        self.lock.acquire()
        try:
            old_store = self.stores_dict.get(store.store_id, None)
            if not old_store:
                # Add any new values previously empty and update any existing values
                #     old_store.merge(store)
                # else:
                self.stores_dict[store.store_id] = store
        finally:
            self.lock.release()


    def add_stores(self, stores):
        """ Adds multiple stores to the data set. Just a masked call to add_store, so same add/update behavior.

            :param stores: stores to add to the data set - list<Store>
        """
        for store in stores:
            self.add_store(store)
