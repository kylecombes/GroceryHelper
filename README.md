# Grocery Helper
[Maggie Rosner](https://github.com/MargaretRosner), [Elena Meyerson](https://github.com/elenameyerson), [Kyle Combes](https://github.com/kylecombes), and [Nina Tchirkova](https://github.com/ntchirkova)

Grocery Helper assists you in planning your grocery shopping. Given a list of items and a location, it will tell you
which stores nearby carry the items and what the best itinerary is to go about purchasing them.

## Project Website

More details on this project can be found [here](http://groceryhelper-sd2017.herokuapp.com/).

## Setup Instructions

#### Dependencies

In order to run GroceryHelper on your own computer, you'll need the following Python 3 modules installed:
  * flask
  * untangle
  * requests

#### API Keys

Then you'll need to create a file called `keys.py` in your project root and put the necessary API keys in it. For the sake
of saving the SoftDes grading team the trouble of manually getting all of the keys, you can simply copy the contents
of [this Google Doc](https://docs.google.com/document/d/1CoLgeVISs_3jkKawN0QK7c0uk9-bWKhPH5vhuYr56XE/edit?usp=sharing)
 and paste it into `keys.py`. (Note: The Doc will be made private again after June 1, 2017.)

#### Setting Up the Database

In preparation for running the web app, you'll need to create the stores and items database and download the nearby stores
data. To do that, just run `python3 setup.py`. It will download and install all the necessary data.

By default it will just download stores in Massachusetts. If you want to add a different ZIP range, simply run
`python3 update_db.py`, using the optional arguments`--start-zip` and `--end-zip` to specify the range of ZIP codes
to pull stores for. Using the argument `--workers` will set the number of simultaneous requests to make while doing so.
Running the script without any arguments is the same as running `python3 update_db.py --start-zip 2000 --end-zip 3000 --workers 100`.

#### Launching the Web App

To actually launch the web app, simply run `python3 webapp_flask.py`. Then visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
in your web browser. Click the "Get Started" tab to a

## Architecture Review
The Architecture Review Preparation and Framing document can be found [here](documentation/ArchReviewPrepFraming.md).

## Architecture Review Reflection and Synthesis
Notes and reflection from the Architecure Review can be found [here](documentation/ArchReviewSynth.md).

## Link to Poster
[poster](https://drive.google.com/open?id=0B33rktaN0ltBUWNONmhKMDRNLW8)
