from geolocation import Geolocation
from database import StoreInfoAccessor


def find_routes_given_ingredients(user_location, ingredients):
    """ Finds the best driving routes for the user to purchase
        all the needed ingredients.
        :param user_location: the user's starting location - Location
        :param ingredients: the ingredients the user needs - list
        :return a list of routes, sorted best to worst
    """
# TODO Fill this out
pass


def get_stores_near_me(my_loc, radius, number):
    """ Get stores within a certain radius of user location.
        :param my_loc: location of the user - Location
        :param radius: search radius (miles)
        :param number: maximum number of stores to return
    """
    stores = StoreInfoAccessor().get_all_stores()
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
