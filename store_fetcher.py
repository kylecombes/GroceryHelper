import requests
import untangle

from simple_models import Location, Store
from supermarket_api_base import SupermarketAPIBase


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
                loc = Location()
                loc.street_address = address
                loc.city = city
                loc.state = state
                loc.zipcode = zipcode
                store = Store()
                store.store_id = store_id
                store.name = name
                store.location = loc
                stores.append(store)
        except IndexError:
            pass

        return stores
