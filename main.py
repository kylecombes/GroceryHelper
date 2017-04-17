from planner.models import Store, Location
from geolocation import Geolocation


class Main:

    @staticmethod
    def get_stores_near_me(my_loc, radius, number):
        """ Get stores within a certain radius of user location.
            :param my_loc: location of the user - Location
            :param radius: search radius (miles)
            :param number: maximum number of stores to return
        """
        stores = list(Store.objects.filter(location__state=my_loc.state))
        stores_in_range = []
        euc_dists = {}
        for s in stores:
            dist = Geolocation.get_euclidean_dist(my_loc, s.location)
            if dist <= radius:
                euc_dists[s.store_id] = dist
                stores_in_range.append(s)

        # Sort according to Euclidean distance
        stores_in_range.sort(key=lambda store: euc_dists[store.store_id])

        # Return the top _number_ of stores
        return stores_in_range[:number]
