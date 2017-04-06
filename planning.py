import copy


class TripPlanner:

    def __init__(self, stores, starting_location, items_needed):
        self.stores = stores
        self.starting_location = starting_location
        self.items_needed = items_needed

    def find_paths(self, base_plan, visited, items_needed):
        """ Recursively finds all the paths to other stores starting at a given store.

            :param base_plan: a TripPlan to extend - TripPlan
            :param visited: dictionary of Stores visited (key is store ID) - [int: Store]
            :param items_needed: list of items still needed - [string?]  # TODO Decide on type for item
            :return list of TripPlans
        """
        possible_paths = list()
        for next_store in self.stores:
            if next_store not in visited:
                visited.append(next_store)
                # Get list of items available at this store
                items_here = None  # TODO
                # Check to make sure this store has some items, otherwise skip it
                if items_here == 0:
                    continue

                # Figure out which items we have left to get
                items_left = [item for item in items_needed not in items_here]

                # Now plan paths to all of the unvisited stores
                new_plans_from_here = self.find_paths(next_store, copy.copy(visited), items_left)
                for plan_extension in new_plans_from_here:
                    base_plan_copy = TripPlan(base_plan=base_plan)
                    possible_paths.append(TripPlan.combine(base_plan_copy, plan_extension))

        return possible_paths


class TripPlan:

    def __init__(self, **options):
        if options['base_plan']:  # We're extending an existing route
            base_plan = options['base_plan']
            self.first_stop = base_plan.first_stop  # TODO Probably going to run into referencing problems. Need to copy base_plan?
            self.last_stop = base_plan.last_stop
            self.score = base_plan.score
        elif options['first_stop']:  # We're starting a new route, and we know our first stop
            self.first_stop = options['first_stop']
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

    @staticmethod
    def combine(first_plan, second_plan):
        """ Combines the two TripPlans into one. """
        first_plan.last_stop = second_plan.first_stop
        second_plan.first_stop = first_plan.last_stop

    @staticmethod
    def clone(first_stop):
        """ Creates a new copy this plan.

            :param first_stop: the first stop in the trip
            :return a new TripPlan with the same attributes as the old one
        """
        first_stop_new = TripStop(first_stop.prev_stop, first_stop.store, first_stop.dist_from_prev, first_stop.score)
        prev_stop = first_stop_new
        while prev_stop.next_stop:
            prev_stop.next_stop = TripStop(prev_stop.prev_stop, prev_stop.store, prev_stop.dist_from_prev, prev_stop.score)
        return first_stop_new


class TripStop:
    """ Node for planning trips """

    def __init__(self, prev_stop, store, dist_from_prev, score):
        """
        :param prev_stop: previous stop on this trip - TripStop
        :param store: store at this stop - Store
        :param dist_from_prev: distance from previous - int
        :param score: score of this store given item needs - int
        """
        self.prev_stop = prev_stop
        self.store = store
        self.dist_from_prev = dist_from_prev
        self.score = score
        self.next_stop = None



