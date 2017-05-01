# from keys import *
import untangle
import requests
from models import *
from xml.sax._exceptions import SAXParseException
import threading


def store_has_ingredient(ingredient, store_id):
    """Given an ingredient and a store id, returns True is item is at that store and False if it is not"""
    #store_id is store id
    foods_at_store = []
    url = format_food_url(store_id, ingredient)
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


def check_store_for_ingredient(store, ingredient):
    print('Checking store for ingredient {}'.format(ingredient))
    if store_has_ingredient(ingredient, store.store_id):
        store.items.append(ingredient)
    print('Done checking store')


def where_are_ingredients(ingredients, stores):
    """ Given a list of stores objects and ingredients returns dictionary of ingredients with stores_ids as values"""

    main_thread = threading.current_thread()
    for store in stores:
        for ing in ingredients:
            check_store_for_ingredient(store, ing)
            # t = threading.Thread(target=check_store_for_ingredient, args=(store, ing))
            # t.start()

        # Wait till all threads finish before continuing
        # for t in threading.enumerate():
        #     if t is not main_thread:
        #         t.join()
        print('Finished processing store')

    return stores


def format_food_url(store_id, food):
    """formats url to make an api request so that """
    base_url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY="
    store = "&StoreId=" + str(store_id)
    food = "&ItemName=" + food
    return base_url + SUPERMARKET_API_KEY + store + food


if __name__ == '__main__':
    ingredients = ["cherry", "arugala", "cucumber", "coke", "cheddar cheese"]
    store = Store('e6k3fjw75k', 'Roche Bros', '1000 Olin Way')
    items_found = where_are_ingredients(ingredients, [store])
    for item in items_found:
        print(item)
