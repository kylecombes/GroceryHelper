from keys import *
from urllib.request import urlopen


def get_ingredients(ingredients, store_id):
    #store_id is store id
    foods_at_store = []
    for food in ingredients:
        url = format_food_url(store_id, food)
        food_string = str(urlopen(url))
        print(food_string)
        food_index = food_string.index('<Itemname>') + len("<Itemname>")
        if not food_string[food_index:food_index+len('NOITEM')] == 'NOITEM':
            foods_at_store.append(food)
    return foods_at_store


def format_food_url(store_id, food):
    base_url = "http://www.SupermarketAPI.com/api.asmx/SearchForItem?APIKEY="
    key = SUPERMARKET_API_KEY
    store = "StoreId=" + str(store_id)
    food = "&ItemName=" + food
    return base_url + SUPERMARKET_API_KEY + store + food

ingredients = ["cherry", "arugala", "cucumber", "coke", "cheddar cheese"]
print(get_ingredients(ingredients, 'e6k3fjw75k'))
