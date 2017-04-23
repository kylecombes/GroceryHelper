from models import *
from flask import Flask, current_app
from database import StoreInfoAccessor, LocationInfoAccessor

app = Flask(__name__)

with app.app_context():
    sia = StoreInfoAccessor()
    my_zip = 2492
    try:
        loc = Location('1000 Olin Way', 'Needham', 'MA', my_zip)
        store = Store('afefesds', 'Marshalls', loc)
        stores = sia.get_stores_in_zip_range(my_zip-200, my_zip+200)
        for store in stores:
            print(store)
    finally:
        sia.close()

