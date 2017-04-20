from models import Location
from flask import Flask, current_app
from database import StoreInfoAccessor

app = Flask(__name__)

with app.app_context():
    db = StoreInfoAccessor()
    try:
        stores = db.get_all_stores()
        for store in stores:
            print(store)
    finally:
        db.close()

