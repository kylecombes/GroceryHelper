#!/bin/bash
## This script sets up the database or performs any
## migrations needed to update it.

my_dir="$(dirname "$0")"

# Determine what needs to be created/changed
python "$my_dir/manage.py" makemigrations

# Do it
python "$my_dir/manage.py" migrate