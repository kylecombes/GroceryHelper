from main import *
from planning import TripPlanner
from models import Store

app = Flask(__name__)

with app.app_context():
    user_loc = Location('1000 Olin Way', 'Needham', 'MA', 2492, 1, 1)
    # Geolocation.load_lat_long_for_location(user_loc)
    # stores = get_stores_near_me(user_loc, 10, 20)

    # loc1 = Location('Stop 1', None, None, None, 1, 3)
    # store1 = Store(1, 'Store 1', loc1)
    # stores[1].items = ['A', 'C', 'B']
    # loc2 = Location('Stop 2', None, None, None, 2, 3.5)
    # store2 = Store(2, 'Store 2', loc2)
    # stores[2].items = ['A', 'D']
    # loc3 = Location('Stop 3', None, None, None, 2, 5)
    # store3 = Store(3, 'Store 3', loc3)
    # stores[3].items = ['D']
    # loc4 = Location('Stop 4', None, None, None, 4, 3.5)
    # store4 = Store(4, 'Store 4', loc4)
    # loc5 = Location('Stop 5', None, None, None, 8, 1)
    # store5 = Store(5, 'Store 5', loc5)
    # store5.items = ['B']
    # loc6 = Location('Stop 6', None, None, None, 6, 4.5)
    # store6 = Store(6, 'Store 6', loc6)
    # loc7 = Location('Stop 7', None, None, None, 2.5, 7)
    # store7 = Store(7, 'Store 7', loc7)
    # loc8 = Location('Stop 8', None, None, None, 5.5, 6)
    # store8 = Store(8, 'Store 8', loc8)
    needed_items = ['A', 'B', 'C', 'D']
    # stores = [store1, store2]#, store3, store4, store5, store6, store7, store8]
    # planner = TripPlanner(user_loc)
    # plans = planner.find_routes(needed_items, stores, 100)

    routes = find_routes_given_ingredients(user_loc, needed_items)
    stops = routes[0].get_stops_as_list()
    for stop in stops:
        if stop.store:
            print(stop.store)
        else:
            print(stop.location)
