from keys import *
import untangle
import requests


def get_ingredients(ingredients, store_id):
    #store_id is store id
    foods_at_store = []
    for food in ingredients:
        url = format_food_url(store_id, food)
        xml_string = requests.get(url).text
        foods = untangle.parse(xml_string)
        for item in foods.ArrayOfProduct.Product:
            store = {
                'aisle': item.AisleNumber.cdata,
                'category': item.ItemCategory.cdata,
                'item_id': item.ItemID.cdata,
                'description': item.ItemDescription.cdata,
                'image': item.ItemImage.cdata,
                'name': item.Itemname.cdata
            }
            foods_at_store.append(store)
    return foods_at_store


def format_food_url(store_id, food):
    base_url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY="
    store = "&StoreId=" + str(store_id)
    food = "&ItemName=" + food
    return base_url + SUPERMARKET_API_KEY + store + food

ingredients = ["cherry"]#, "arugala", "cucumber", "coke", "cheddar cheese"]
items_found = get_ingredients(ingredients, 'e6k3fjw75k')
print(items_found)
