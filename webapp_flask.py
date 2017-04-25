"""
webapp for GroceryHelper Project Flask Code
"""

from flask import Flask

import json
import math
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import urlopen

from keys import *

from geolocation import Geolocation
from database import StoreInfoAccessor
from models import Location, Store
from flask import render_template
from flask import request
from models import Location
from planning import TripPlan, TripStop
from main import find_routes_given_ingredients

app = Flask(__name__)

@app.route('/')
#def hello_world():
def starting_page():
    return render_template('about.html')

@app.route('/app', methods=['GET','POST'])
def webapp():
    if request.method == 'POST':
        #if request.form['index.html']:
        return redirect(url_for('index'))
    return render_template('index.html')
    #'The about page'

@app.route('/about_project', methods=['GET','POST'])
def webapp_about():
    if request.method == 'POST':
        #if request.form['index.html']:
        return redirect(url_for('about_team'))
    return render_template('about_team.html')
    #'The about page'

@app.route('/about_us', methods=['GET','POST'])
def webapp_about_us():
    if request.method == 'POST':
        #if request.form['index.html']:
        return redirect(url_for('about_us'))
    return render_template('about_us.html')
    #'The about page'

@app.route('/login', methods=['GET','POST'])
def login():
   error = None
   if request.method == 'POST':
       if request.form['Yes!']:
           error = None
           return render_template('address_input.html')
       else:
           error = None
           return render_template('index.html')

@app.route('/input', methods=['GET','POST'])
def input():
  error = None
  if request.method == 'POST':
      if request.form['No']:
          error = None
          return render_template('food_input.html')
      else:
          error = None
          return render_template('index.html')


@app.route('/food', methods=['GET','POST'])
def getting_food(location=None,stops=None,cuisine=None, src=None):
  error = None
  if request.method == 'POST':
      if request.form['type'] and request.form['housenum'] and request.form['street'] and request.form['city'] and request.form['state'] and request.form['zip']:
          error = None

          zipcode = int(request.form['zip'])
          cuisine = str(request.form['type'])
          street_address = str(request.form['housenum'] + ' ' + request.form['street'])
          city = str(request.form['city'])
          state = str(request.form['state'])
          # format ingredients
          ingredients = request.form['ingredients']
          ingredients = ingredients.split(" ")
          ingredients = ", ".join(ingredients) #for word in ingredients])
          #print(ingredients)

          loc = Location(street_address, city, state, zipcode)
          #print(loc)
          routes = find_routes_given_ingredients(loc, ingredients)
          stops = routes.get_stops_as_list()

          src = Geolocation.get_directions(loc, ["1000 Olin Way", "Boston College"])
          return render_template('confirm2.html', location=loc, stops=stops,cuisine=cuisine, src=src)


      else:
          return render_template('food_input.html')

@app.route('/address', methods=['GET','POST'])
def getting_address(location=None, stops=None, src=None):
    error = None
    if request.method == 'POST':
        if request.form['ingredients'] and request.form['housenum'] and request.form['street'] and request.form['city'] and request.form['state'] and request.form['zip']:
            error = None

            zipcode = int(request.form['zip'])
            street_address = str(request.form['housenum'] + ' ' + request.form['street'])
            city = str(request.form['city'])
            state = str(request.form['state'])

            ingredients = str(request.form['ingredients'])
            ingredients = ingredients.split(" ")
            ingredients = ", ".join(ingredients)

            loc = Location(street_address, city, state, zipcode)
            results = find_routes_given_ingredients(loc, ingredients)
            stops = results.get_stops_as_list()
            print('wut')
            print(stops)
            # stops = TripStop(None, 'Safeway', 'Tacoma', '10 miles', '10')
            # loc = str(street_address + ' ' + city + ' ' + state)

            src = Geolocation.get_directions(loc, stops)

            return render_template('confirm.html', location=loc, stops=stops, src=src)

        else:
          error = None
          return render_template('address_input.html')

#
#     the code below is executed if the request method
#     was GET or the credentials were invalid
if __name__ == '__main__':
    app.run()
