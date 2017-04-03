"""Use this file for Recipe and Recipe API related stuff."""


"""
Defines code that takes in recipe or cuisine from user and outputs
a list of ingredients that can be used by store finder algorithm.
URL coded for Yummly API, still waiting to hear back with API key though.
"""
def userInput():
    pass
    ###integrate with Nina's code but add extra input sections


def encodeURL_Yummly(search, allowed_ingredients, allowed_cuisines):
    BASE_URL = "http://api.yummly.com/v1/api/recipes?_app_id=app-id&_app_key=app-key&"
    ### make sure to add in API key ^^^^
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

def encodeURL_Campbells(search, ingredients):
    BASE_URL = "http://api.campbellskitchen.com/api/BrandService.svc/"
    search = search.replace(" ", "%20")

    inglist = ""
    for ing in ingredients:
        inglist = ing + "|"

    url = BASE_URL + "/search?ingredient=" + inglist + "&app_id=45d2a062&app_key=%s"% (RECIPE_API_KEY)

"""To Do: figure out calling api key from file, add inputs for other types of searches"""

def callAPI(url):
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data


def returnIngredients(response_data):
    pass
    #ingredientLines from the output data


#print(encodeURL('fried chicken', ['apples','chicken','butter'], ['Southern']))
print(encodeURL_Campbells('green', ['bean', 'chicken', 'lettuce']))
