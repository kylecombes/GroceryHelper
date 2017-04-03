"""Code map for final project, Will be filled in as we write methods and test."""

class Location:

    def get_user_input():
        pass

class Geocode:

    def get_lat_lon():
        pass

    def get_addr():
        pass

    def get_dist():
        pass



"""
Defines back end code that takes in recipe or cuisine from user and outputs
a list of ingredients that can be used by store finder algorithm.
"""
def userInput():
    pass
    ###integrate with Nina's code but add extra input sections


def encodeURL(search, allowed_ingredients, allowed_cuisines):
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


def callAPI(url):
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, "utf-8"))
    return response_data


print(encodeURL('fried chicken', ['apples','chicken','butter'], ['Southern']))
