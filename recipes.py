"""Use this file for Recipe and Recipe API related stuff."""


"""
Defines code that takes in recipe or cuisine from user and outputs
a list of ingredients that can be used by store finder algorithm.
URL coded for use with Yummly API.
Defines Recipe class that holds information about each recipe (name, ID,
ingredients, cuisine, source website, and image)
"""

from urllib import urlopen
import json


"""
Encodes URL using user input for use with Yummly API.
"""

def encodeURL_Yummly(search, allowed_ingredients, allowed_cuisines):
    f = open('keys.py')
    getKeys= f.read()
    index = getKeys.find('YUMMLY_API_KEY = ')
    API = getKeys[86+18:-2]
    f.close()

    BASE_URL = "http://api.yummly.com/v1/api/recipes?_app_id=55f87b35&_app_key=%s&"% (API)
    search = search.replace(" ", "+")
    ingred = ""
    cuisines = ""
    for ing in allowed_ingredients:
        ing = ing.replace(" ", "+");
        ingred += "&allowedIngredient[]=" + ing

    for cuis in allowed_cuisines:
        cuis = cuis.replace(" ", "+")
        cuis = cuis.lower()
        cuisines += "&allowedCuisine[]=cuisine^cuisine-" + cuis

    url = BASE_URL + "q=" + search + ingred + cuisines
    return url


"""
Calls API using formatted URL and returns data in JSON format.
returnInformation formats data into a usable list.
"""

def callAPI(url):
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text)) #, "utf-8"
    return response_data


def returnInformation(response_data):
    name = response_data['matches'][0]['recipeName']
    recipeID = response_data['matches'][0]['id']
    ingredients = response_data['matches'][0]['ingredients']
    cuisine = response_data['matches'][0]['attributes']['cuisine'][0]
    source = response_data['matches'][0]['sourceDisplayName']
    imageURL = response_data['matches'][0]['imageUrlsBySize']['90']
    information = [name, recipeID, ingredients, cuisine, source, imageURL]
    return information


"""
Defines Recipe class to hold recipe data.
"""

class Recipe():
    def __init__(self, name, recipeID, ingredients, cuisine, source, imageURL):
        self.name = name
        self.recipeID = recipeID
        self.ingredients = ingredients
        self.cuisine = cuisine
        self.source = source
        self.imageURL = imageURL

    def __str__(self):
        return self.name


#url = encodeURL_Yummly('stir fry', ['apples','chicken','butter'], ['asian'])
#friedChicken = Recipe(returnInformation(callAPI(url))[0],returnInformation(callAPI(url))[1], returnInformation(callAPI(url))[2], returnInformation(callAPI(url))[3], returnInformation(callAPI(url))[4], returnInformation(callAPI(url))[5])
#print(friedChicken)
#print(callAPI(url))
#print(encodeURL_Campbells('green', ['bean', 'chicken', 'lettuce']))
