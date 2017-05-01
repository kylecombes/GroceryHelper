"""
webapp for GroceryHelper Project Flask Code
"""

from flask import Flask
import os
from geolocation import Geolocation
from flask import render_template, request
from models import Location
from main import find_routes_given_ingredients
from database import DatabaseAccessor

HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

if not os.path.exists(DatabaseAccessor.DATABASE_PATH):
    import setup

@app.route('/')
#def hello_world():
def starting_page():
    return render_template('about.html')

@app.route('/app', methods=['GET','POST'])
def webapp():
    if request.method == 'POST':
        #if request.form['get_started.html']:
        return redirect(url_for('index'))
    return render_template('get_started.html')
    #'The about page'

@app.route('/about_project', methods=['GET','POST'])
def webapp_about():
    if request.method == 'POST':
        #if request.form['get_started.html']:
        return redirect(url_for('about_team'))
    return render_template('about_project.html')
    #'The about page'

@app.route('/about_us', methods=['GET','POST'])
def webapp_about_us():
    if request.method == 'POST':
        #if request.form['get_started.html']:
        return redirect(url_for('about_us'))
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
           return render_template('get_started.html')

@app.route('/input', methods=['GET','POST'])
def input():
  error = None
  if request.method == 'POST':
      if request.form['No']:
          error = None
          return render_template('food_input.html')
      else:
          error = None
          return render_template('get_started.html')


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
              stops_print.append(str(stop))
              stops_print = stops_print.split(',')
          print(stops_print)

          return render_template('confirm2.html', location=loc, stops=stops_print,cuisine=cuisine, src=src)

      else:
          return render_template('food_input.html')

@app.route('/address', methods=['GET','POST'])
def getting_address(location=None, stops=None, src=None):

    if request.method == 'POST':
        if request.form['ingredients'] and request.form['housenum'] and request.form['street'] and request.form['city'] and request.form['state'] and request.form['zip']:

            zipcode = int(request.form['zip'])
            street_address = str(request.form['housenum'] + ' ' + request.form['street'])
            city = str(request.form['city'])
            state = str(request.form['state'])

            ingredients = str(request.form['ingredients'])

            loc = Location(street_address, city, state, zipcode)
            did_find_items, results = find_routes_given_ingredients(loc, ingredients)

            print('Found {} possible routes'.format(len(results)))

            if not did_find_items:
                stops_html = '<p>Could not find item "{}" anywhere.'.format(results)

            elif len(results) > 0:
                stops = results[0].get_stops_as_list()

                num_stops = len(stops)
                if num_stops > 0:
                    src = Geolocation.get_directions(loc, stops)
                    stops_html = ''
                    for i in range(1, num_stops):
                        stop_html = get_html_for_stop(stops[i], i)
                        stops_html = '{}{}\n'.format(stops_html, stop_html)  # Append stop HTML
                else:
                    stops_html = '<p>No viable routes found</p>'
                    src = ''
            else:
                stops_html = '<p>No viable routes found</p>'


            return render_template('confirm.html', location=loc, stops=stops_html, src=src)

        else:
          return render_template('address_input.html')


def get_html_for_stop(stop, i):
    if stop.store:
        name = stop.store.name
        items = stop.get_items_as_string()
    else:
        name = 'Home'
        items = ''
    html = '<div class="trip-stop">' \
           '<span class="stop-number">{stopnum}</span>' \
           '<div class="store-info">'\
           '<span class="store-name">{name}</span>' \
           '<span class="store-location">{location}</span>' \
           '<div class="items-at-store">{items}</div>' \
           '</div>' \
           '<span class="stop-dist">{dist:0.1f} miles</span>' \
           '</div>' \
           .format(
                stopnum=i,
                name=name,
                items=items,
                location=stop.location,
                dist=stop.dist_from_prev
           )
    return html



#
#     the code below is executed if the request method
#     was GET or the credentials were invalid
if __name__ == '__main__':
    # HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    # PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
