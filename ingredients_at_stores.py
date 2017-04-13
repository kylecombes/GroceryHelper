from keys import *
import untangle
import requests


def get_ingredients(ingredients, store_id):
    """Given a list of ingredients and a store id, returns a list of ingredients at that store
    * each ingredient is a dictionary with a keys: category, item_id and name"""
    #store_id is store id
    foods_at_store = []
    for food in ingredients:
        url = format_food_url(store_id, food)
        xml_string = requests.get(url).text
        foods = untangle.parse(xml_string)
        for item in foods.ArrayOfProduct.Product:
            f = {
                'category': item.ItemCategory.cdata,
                'item_id': item.ItemID.cdata,
                'name': item.Itemname.cdata
            }
            foods_at_store.append(f)
    return foods_at_store

def where_are_ingreidients(ingredients, stores):
    """ Given a list of stores ids and ingredients returns dictionary of ingredients with stores_ids as values"""
    inventory = {}
    for s in stores:
        foods = get_ingredients(ingredients, s)
        for f in foods:
            inventory[f['name']] = s
    return inventory




def format_food_url(store_id, food):
    """formats url to make an api request so that """
    base_url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY="
    store = "&StoreId=" + str(store_id)
    food = "&ItemName=" + food
    return base_url + SUPERMARKET_API_KEY + store + food

ingredients = ["cherry"]#, "arugala", "cucumber", "coke", "cheddar cheese"]
items_found = get_ingredients(ingredients, 'e6k3fjw75k')
print(items_found)
