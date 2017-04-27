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
          stops = find_routes_given_ingredients(loc, ingredients)
          src = Geolocation.get_directions(loc, stops)

          stops_print = []
          for stop in stops:
              stops_print.append(TripStop.get_string(stop))
              stops_print = stops_print.split(',')
          print(stops_print)

          return render_template('confirm2.html', location=loc, stops=stops_print,cuisine=cuisine, src=src)

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
            stops = find_routes_given_ingredients(loc, ingredients)
            #stops = results.get_stops_as_list()

            # print('wut')
            # for stop in stops:
            #     stops = TripStop(results.last_stop, stop, stop.location, 13, 0.452)
            #return stops
            # stops = TripStop(None, 'Safeway', 'Tacoma', '10 miles', '10')
            # loc = str(street_address + ' ' + city + ' ' + state)

            src = Geolocation.get_directions(loc, stops)
            stops_html = '\n'.join(get_html_for_stop(s) for s in stops)


            return render_template('confirm.html', location=loc, stops=stops_html, src=src)

        else:
          error = None
          return render_template('address_input.html')


def get_html_for_stop(stop):
    html = '<div class="trip-stop">' \
           '<div class="store-info">'\
           '<span class="store-name">{name}</span>' \
           '<span class="store-location">{location}</span>' \
           '</div>' \
           '<span class="stop-dist">{dist}</span>' \
           '</div>' \
           .format(
                name=stop.store.name,
                location=stop.location,
                dist=stop.dist_from_prev
           )
    return html



#
#     the code below is executed if the request method
#     was GET or the credentials were invalid
if __name__ == '__main__':
    app.run()
