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

@app.route('/about_team', methods=['GET','POST'])
def webapp_about():
    if request.method == 'POST':
        #if request.form['index.html']:
        return redirect(url_for('about_team'))
    return render_template('about_team.html')
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
def getting_food(location=None,stops=None,cuisine=None):
  error = None
  if request.method == 'POST':
      if request.form['type'] and request.form['housenum'] and request.form['street'] and request.form['city'] and request.form['state'] and request.form['zip']:
          error = None

        #   zipcode = int(request.form['zip'])
          cuisine = request.form['type']
        #   street_address = request.form['housenum'] + ' ' + request.form['street']
        #   city = request.form['city']
        #   state = request.form['state']
        #   ingredients = request.form['ingredients']
          #
          #
        #   loc = Location(street_address, city, state, zipcode)
        #   results = find_routes_given_ingredients(loc, ingredients)
        #   trip_stops = get_stops_as_list(results)

          trip_stops = "testing displaying the stops"
          loc = "testing displaying the location"

          #convert zip to integer
          #loc = Location('street'....)#check order in top level of models.py
          #send loc data to find_routes_given_ingredients in main
          #result of sending data is an object I can call get_stops_as list on
          #call method get_stops as list it will return a list of trip stops
          #in tripstop class you can get a list of trip stops
          #import find routes to user location and pass in the loc and list of ingredients

          return render_template('confirm2.html', location=loc, stops=trip_stops, cuisine=cuisine)
      else:
          error = None
          return render_template('food_input.html')

@app.route('/address', methods=['GET','POST'])
def getting_address(location=None,stops=None):
  error = None
  if request.method == 'POST':
      if request.form['housenum'] and request.form['street'] and request.form['city'] and request.form['state'] and request.form['zip']:
          error = None

          zipcode = int(request.form['zip'])
          street_address = str(request.form['housenum'] + ' ' + request.form['street'])
          city = str(request.form['city'])
          state = str(request.form['state'])
          ingredients = str(request.form['ingredients'])
          type_check = type(zipcode)

          ##throwing an internal error when I try with random addresses. I think there are
          ##only specific ones I can use from a dataset...
          loc = Location(street_address, city, state, zipcode)
          results = find_routes_given_ingredients(loc, ingredients)
          trip_stops = get_stops_as_list(results)

        #   trip_stops = "testing displaying the plan"
        #   loc = "testing displaying the user location"

          return render_template('confirm.html', location=loc, stops=trip_stops)

            #convert zip to integer
            #loc = Location('street'....)#check order in top level of models.py
            #send loc data to find_routes_given_ingredients in main
            #result of sending data is an object I can call get_stops_as list on
            #call method get_stops as list it will return a list of trip stops
            #in tripstop class you can get a list of trip stops
            #import find routes to user location and pass in the loc and list of ingredients
            #now that all of the inputs from the user are accounted for call the code function

      else:
          error = None
          return render_template('address_input.html')

#
#     the code below is executed if the request method
#     was GET or the credentials were invalid
if __name__ == '__main__':
    app.run()
