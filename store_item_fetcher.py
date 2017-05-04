import untangle
import requests
from xml.sax._exceptions import SAXParseException
import threading
from database import FoodItemInfoAccessor
from import_keys import *


class StoreItemFetcher:

    def __init__(self, use_api=False):
        """
        Initializes a StoreItemFetcher to get information about items at stores.
        :param use_api: if True, will use the Supermarket API, otherwise just uses the grocery UPC database from grocery.com
        """
        self.use_api = use_api


    def check_stores_for_ingredients(self, ingredients, stores):
        """ Given a list of stores objects and ingredients returns dictionary of ingredients with stores_ids as values"""

        if self.use_api:  # Use Supermarket API
            main_thread = threading.current_thread()
            for store in stores:
                for ing in ingredients:
                    # StoreItemFetcher._check_store_for_items(store, ing)
                    t = threading.Thread(target=StoreItemFetcher._check_store_for_items, args=(store, ing))
                    t.start()

                # Wait till all threads finish before continuing
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()
                print('Finished processing store')

        else:  # Use the local database
            fia = FoodItemInfoAccessor()
            store_groups = self.__filter_stores_and_group(stores)
            for ingredient in ingredients:
                results = fia.get_foods_by_name(ingredient)
                if len(results) > 0:
                    print('Added food to {} stores'.format(self.__add_food_to_appropriate_stores(results, store_groups, ingredient)))
                else:
                    return False, ingredient

        return True, stores

    def __filter_stores_and_group(self, stores):
        """
        Adds a food item (likely pulled from the database with no store association) to the "appropriate" stores.
        :param foods: a list of all the FoodItems found when querying the database - [FoodItem]
        :param stores: the stores to potentially add the food to - [Store]
        :return: None (the stores are updated in-place)
        """
        # Do arbitrary filtering so not every item is available at every store
        store_count = len(stores)
        # if len(foods) > 3 * store_count:  # Just cut out some items if we have way more results than stores
        #     for i in range(0, len(foods)-3, 3):
        #         foods[i].remove()

        # Group the stores according to a property of their IDs (e.g. if the remainder when divided by a certain number - totally arbitrary)
        store_groups = dict()
        mod = int(store_count / 3) + 1
        for store in stores:
            try:  # See if the store ID is hex (most are)
                store_id = int('0x' + store.store_id, 16)
                group_num = store_id % mod
            except ValueError:  # If not hex, just assign it to group 0
                group_num = 0
            if group_num not in store_groups:
                store_groups[group_num] = list()
            store_groups[group_num].append(store)

        return list(store_groups.values())

    def __add_food_to_appropriate_stores(self, foods, store_groups, query):
        """
        Adds a food item (likely pulled from the database with no store association) to the "appropriate" stores.
        :param food: a list of all the FoodItems found when querying the database - [FoodItem]
        :param groups: the stores to potentially add the food to - [Store]
        :return: None (the stores are updated in-place)
        """
        num_groups = len(store_groups)
        num_items = len(foods)
        added_count = 0
        if num_groups > 0:
            interval = int(num_items/6) if num_items > 6 else 1
            for i in range(0, num_items - interval, interval):
                food_item = foods[i]
                group = food_item.id % num_groups
                stores = store_groups[group]
                for store in stores:
                    if query not in store.items:
                        store.items.append(query)
                        added_count += 1
        return added_count


    @staticmethod
    def _check_store_for_items(store, ingredient):
        print('Checking store for ingredient {}'.format(ingredient))
        if StoreItemFetcher.does_store_have_item(ingredient, store.store_id):
            store.items.append(ingredient)
        print('Done checking store')

    @staticmethod
    def does_store_have_item(ingredient, store_id):
        """Given an ingredient and a store id, returns True is item is at that store and False if it is not"""
        #store_id is store id
        foods_at_store = []
        url = StoreItemFetcher.format_food_url(store_id, ingredient)
        try:
            xml_string = requests.get(url, timeout=10).text
        except requests.exceptions.Timeout:
            print('Request timed out')
            return False
        try:
            foods = untangle.parse(xml_string)
        except SAXParseException as e:
            print('Invalid response received for store {} looking for {}'.format(store_id, ingredient))
            print('Request URL: ', url)
            print('Response: ', xml_string)
            print(e)
            return False
        for item in foods.ArrayOfProduct.Product:
            f = {
                'category': item.ItemCategory.cdata,
                'item_id': item.ItemID.cdata,
                'name': item.Itemname.cdata
            }
            foods_at_store.append(f)
        if len(foods_at_store) > 0:
            return True
        else:
            return False


    @staticmethod
    def format_food_url(store_id, food):
        """formats url to make an api request so that """
        base_url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY="
        store = "&StoreId=" + str(store_id)
        food = "&ItemName=" + food
        return base_url + SUPERMARKET_API_KEY + store + food

if __name__ == '__main__':
    from flask import Flask, g
    from main import get_stores_near_me
    from models import Location
    from geolocation import Geolocation
    from planning import TripPlanner

    app = Flask(__name__)
    with app.app_context():

        needed_items = ['apples', 'cashews', 'butternut squash']

        try:
            user_loc = Location('1000 Olin Way', 'Needham', 'MA', 2492)
            Geolocation.load_lat_long_for_location(user_loc)
            stores = get_stores_near_me(user_loc, 10, 20)
            # sif = StoreItemFetcher(False)
            # sif.check_stores_for_ingredients(needed_items, stores)
            planner = TripPlanner(user_loc)
            plans = planner.find_routes(needed_items, stores, 20, False)
            for plan in plans:
                print(plan)

        finally:
            db = getattr(g, '_database', None)
            if db:
                db.close()
