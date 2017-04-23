from models import *
from flask import Flask, current_app
from database import StoreInfoAccessor, LocationInfoAccessor

app = Flask(__name__)

with app.app_context():
    sia = StoreInfoAccessor()
    try:
        loc = Location('1000 Olin Way', 'Needham', 'MA', 2492)
        store = Store('afefesds', 'Marshalls', loc)
        sia.save_store(store, LocationInfoAccessor())
        stores = sia.get_all_stores()
        for store in stores:
            print(store)
    finally:
        sia.close()

