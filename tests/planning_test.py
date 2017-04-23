from main import *

app = Flask(__name__)

with app.app_context():
    user_loc = Location('1000 Olin Way', 'Needham', 'MA', 2492)
    stores = get_stores_near_me(user_loc, 100, 20)
    for store in stores:
        print(store)

