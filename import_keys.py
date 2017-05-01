import os
if 'MAPS_API_KEY' not in os.environ:  # Don't run on Heroku
    from keys import *
else:
    SUPERMARKET_API_KEY = os.environ['SUPERMARKET_API_KEY']

    KEY_GEO = os.environ["KEY_GEO"]
    KEY_DIST = os.environ["KEY_DIST"]
    KEY_DIRECT = os.environ["KEY_DIRECT"]

    RECIPE_API_KEY = os.environ['RECIPE_API_KEY']
    YUMMLY_API_KEY = os.environ['YUMMLY_API_KEY']
    MAPS_API_KEY = os.environ['MAPS_API_KEY']
    MAPS_EMBED_KEY = os.environ['MAPS_EMBED_KEY']
