from django.core.management.base import BaseCommand

from main import Main
from models import *
from planning import TripPlanner


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Define the arguments that can be used when running this command
        pass

    def handle(self, *args, **options):
        stores = Store.objects.all()
        # loc1 = stores[1].location
        # loc2 = stores[2].location
        # dist = Geolocation.get_euclidean_dist(loc1, loc2)
        # print('It is {0:0.2f} miles from {1} to {2}.'.format(dist, loc1, loc2))
        my_loc = Location(street_address='1000 Olin Way', city='Needham', state='MA', zipcode=2492)
        stores = Main.get_stores_near_me(my_loc, 300, 10)
        stores[0].items = ['A', 'B', 'C']
        stores[1].items = ['A']
        stores[2].items = ['D']
        items_needed = ['A', 'B', 'C', 'D']
        print('Found {} stores nearby:'.format(len(stores)))
        for store in stores:
            print(store)
        print('Planning route...')
        planner = TripPlanner(my_loc, items_needed)
        routes = planner.find_routes(items_needed, stores, 100)
        print('Done!')
#3f434e2e0d
