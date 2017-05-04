# Grocery Helper
[Maggie Rosner](https://github.com/MargaretRosner), [Elena Meyerson](https://github.com/elenameyerson), [Kyle Combes](https://github.com/kylecombes), and [Nina Tchirkova](https://github.com/ntchirkova)

Grocery Helper assists you in planning your grocery shopping. Given a list of items and a location, it will tell you
which stores nearby carry the items and what the best itinerary is to go about purchasing them.

## Project Website

More details on this project can be found [here](http://groceryhelper-sd2017.herokuapp.com/). (The planner is not quite
live yet, so just steer clear of the _Get Started!_ tab.)

## Setup Instructions

#### Dependencies

In order to run GroceryHelper on your own computer, you'll need the following Python 3 modules installed:
  * flask
  * untangle
  * requests

#### Setting Up the Database

Then, in preparation for running the web app, you'll need to update the nearby stores database. To do that, run
`python3 update_db.py`. You can use the optional arguments`--start-zip` and `--end-zip` to specify the range of ZIP codes
to pull stores for. Using the argument `--workers` will set the number of simultaneous requests to make while doing so.
Running the script without any arguments is the same as running `python3 update_db.py --start-zip 2000 --end-zip 3000 --workers 100`.

Once you've run the above script, the web app will function properly. To add new areas to the web app, simple rerun the
script with a new ZIP range.

## Architecture Review
The Architecture Review Preparation and Framing document can be found [here](documentation/ArchReviewPrepFraming.md).

## Architecture Review Reflection and Synthesis
Notes and reflection from the Architecure Review can be found [here](documentation/ArchReviewSynth.md).

## Link to Poster
[poster](https://drive.google.com/open?id=0B33rktaN0ltBUWNONmhKMDRNLW8)
