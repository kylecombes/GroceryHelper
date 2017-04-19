"""
webapp for GroceryHelper Project Flask Code
"""

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
#def hello_world():
def starting_page():
    return render_template('about.html')

@app.route('/app', methods=['GET','POST'])
def webapp():
    if request.method == 'POST':
        if request.form['index.html']:
            return render_template('index.html')
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
           return render_template('food_input.html')

    #the code below is executed if the request method
    #was GET or the credentials were invalid
if __name__ == '__main__':
    app.run()
