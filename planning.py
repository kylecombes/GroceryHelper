import copy
from geolocation import Geolocation, DistanceMapper
from store_item_fetcher import StoreItemFetcher


class TripPlanner:

    def __init__(self, starting_location, distances=None):
        self.stores = None
        self.starting_location = starting_location
        self.distance_mapper = distances if distances else DistanceMapper()

    def find_routes(self, needed_items, nearby_stores, max_distance, use_api=True):
        """ Finds all the possible routes to purchase the needed items within the specified search radius.
            NOTE: The list of stores passed may include stores outside the search radius. This method will
            filter the list based on search radius before finding routes.
            :param needed_items: list of grocery items needed - [str]
            :param nearby_stores: list of nearby stores - [Store]
            :param max_distance: maximum distance (in miles) of stores from starting location to include in route - int
            :param use_api: whether or not to use the Supermarket API - bool
            :return a list of TripPlans sorted best to worst - [TripPlan]
        """
        # Filter the stores to only include stores with a Euclidean distance within the specified search radius
        self.stores = [store for store in nearby_stores if Geolocation.get_euclidean_dist(self.starting_location, store.location) <= max_distance]

        print('Checking nearest {} stores for the needed items...'.format(len(self.stores)))
        # Load items at stores
        found_all_items, missing_item = StoreItemFetcher(use_api).check_stores_for_ingredients(needed_items, self.stores)

        if not found_all_items:
            print('Could not find item {} anywhere. Aborting.'.format(missing_item))
            return False, missing_item

        print('Calculating the distances between places...')
        # Get distances between places
        locations = [store.location for store in self.stores]
        locations.insert(0, self.starting_location)
        self.distance_mapper.load_distances(locations, locations)

        print('Planning...')
        base_plan = TripPlan(first_stop=self.starting_location)
        routes = self.__find_path_continuations(base_plan, [], needed_items, 2*max_distance)  # Max distance is the diameter of the circle
        # Add returning to the starting point
        for route in routes:
            dist_home = self.distance_mapper.get_distance(route.last_stop.location, self.starting_location)
            home_stop = TripStop(route.last_stop, None, self.starting_location, dist_home, None, 0)
            route.add_stop(home_stop)

        # Sort stores best to worst
        routes.sort(key=lambda r: r.last_stop.dist_from_start)

        return True, routes

    def __find_path_continuations(self, base_plan, visited, items_needed, max_dist_btwn_stops):
        """ Recursively finds all the paths to other stores starting at a given store.

            :param base_plan: a TripPlan to extend - TripPlan
            :param visited: dictionary of Stores visited (key is store ID) - [int: Store]
            :param items_needed: list of items still needed - [string?]  # TODO Decide on type for item
            :return list of TripPlans
        """
        possible_paths = list()
        for next_store in self.stores:
            if next_store not in visited:
                visited_copy = copy.copy(visited)
                visited_copy.append(next_store)
                # Get list of items available at this store
                items_here = next_store.items
                # If this store doesn't have any items, skip it
                if not items_here or len(items_here) == 0:
                    continue

                # Keep track of which items to get here, and which we have left to get
                items_left = list()
                items_to_get_here = list()
                for item in items_needed:
                    if item in items_here:
                        items_to_get_here.append(item)
                    else:
                        items_left.append(item)
                # Calculate distance to here from previous stop
                distance_to_store = self.distance_mapper.get_distance(base_plan.last_stop.location, next_store.location)

                # Get the score for the store
                score = self.__get_store_score(items_here, items_needed, distance_to_store, max_dist_btwn_stops)

                # Add this stop to the plan
                base_plan_copy = copy.deepcopy(base_plan)

                this_stop = TripStop(base_plan_copy.last_stop, next_store, next_store.location, distance_to_store, items_to_get_here, score)
                base_plan_copy.add_stop(this_stop)
                if len(items_left) > 0:
                    # Now plan paths to all of the unvisited stores
                    found_paths = self.__find_path_continuations(base_plan_copy, visited_copy, items_left, max_dist_btwn_stops)

                    for path in found_paths:
                        possible_paths.append(path)
                else:
                    possible_paths.append(base_plan_copy)

        return possible_paths

    # Weights for scoring
    ITEMS_WEIGHT = 0.6
    DISTANCE_WEIGHT = 0.4

    def __get_store_score(self, items_at_store, items_needed, distance_to_store, max_dist_btwn_stops):
        """ Get a score for the store for ranking purposes. Scores range from 0 to 1 (inclusive), with
            1 being optimal and 0 being the worst possible score.
            :param items_at_store: a list of items at the store
            :param items_needed: a list of items still needed
            :param distance_to_store: the distance to the store in miles - int
            :param max_dist_btwn_stops: the maximum distance the user can travel between two stops (used for normalizing distance scores) - int
        """
        # Calculate percentage of items not available at store
        # number_have = len([x for x in items_needed if x not in items_at_store])
        # percent_have = number_have / len(items_needed)

        # Calculate distance score
        distance_score = 1 - distance_to_store / max_dist_btwn_stops

        # Take the weighted average and return the score
        return distance_score#(percent_have * self.ITEMS_WEIGHT + distance_score * self.DISTANCE_WEIGHT)/(self.ITEMS_WEIGHT + self.DISTANCE_WEIGHT)


class TripPlan:

    def __init__(self, **options):
        if 'first_stop' in options:  # We're starting a new route, and we know our first stop
            first_stop_location = options['first_stop']
            self.first_stop = TripStop(None, None, first_stop_location, 0, None, 1)
            self.last_stop = self.first_stop
            self.score = self.first_stop.score
        else:  # We're starting a new route, but we don't know our first stop yet
            self.first_stop = None
            self.last_stop = None
            self.score = 0

    def add_stop(self, new_stop):
        """ Adds a new stop to the plan.

            :param new_stop: the new stop - TripStop
        """
        if self.first_stop:  # Check if we already have at least one stop
            self.last_stop.next_stop = new_stop
            self.last_stop = new_stop
        else:  # No existing stops, so this is our first one
            self.first_stop = new_stop
            self.last_stop = new_stop
        self.score += new_stop.score

    def get_stops_as_list(self):
        """ Returns a list of the stops. """
        stop = self.first_stop
        res = list()
        while stop:
            res.append(stop)
            stop = stop.next_stop
        return res

    @staticmethod
    def combine(first_plan, second_plan):
        """ Combines the two TripPlans into one. """
        first_plan.last_stop = second_plan.first_stop
        second_plan.first_stop = first_plan.last_stop
        return first_plan

    @staticmethod
    def clone(first_stop):
        """ Creates a new copy this plan.

            :param first_stop: the first stop in the trip
            :return a new TripPlan with the same attributes as the old one
        """
        first_stop_new = TripStop(None, first_stop.store, first_stop.store.location, first_stop.dist_from_prev, first_stop.items_to_get, first_stop.score)
        prev_stop = first_stop_new
        while prev_stop.next_stop:
            prev_stop.next_stop = TripStop(prev_stop.prev_stop, prev_stop.store, prev_stop.store.location, prev_stop.dist_from_prev, prev_stop.items_to_get, prev_stop.score)
        return first_stop_new


class TripStop:
    """ Node for planning trips """

    def __init__(self, prev_stop, store, location, dist_from_prev, items_to_get, score):
        """
        :param prev_stop: previous stop on this trip - TripStop
        :param store: store at this stop - Store
        :param location: the location of the stop (could just be the store's location attribute) - Location
        :param dist_from_prev: distance from previous - int
        :param score: score of this store given item needs - int
        """
        self.prev_stop = prev_stop
        self.store = store
        self.location = location
        self.dist_from_prev = dist_from_prev
        self.dist_from_start = (prev_stop.dist_from_start + dist_from_prev) if prev_stop else dist_from_prev
        self.items_to_get = items_to_get
        self.score = score
        self.next_stop = None

    def get_items_as_string(self):
        """ Returns the items as a nicely formatted string for display to the user. """
        if not self.items_to_get or len(self.items_to_get) == 0:
            return 'No needed items found at this store'
        res = 'Get ' + self.items_to_get[0]
        if len(self.items_to_get) == 1:
            return res

        res = res[0].upper() + res[1:]
        for i in range(1, len(self.items_to_get) - 1):
            res = '{}, {}'.format(res, self.items_to_get[i])
        res = '{} and {}'.format(res, self.items_to_get[-1])
        return res

    def __str__(self):
        return '{store} at {location} has a score of {score} and is {dist:0.2f} miles from the last stop.'.format(store=self.store, location=self.location, score=self.score, dist=self.dist_from_prev)
