#!/bin/bash
## This script sets up the database or performs any
## migrations needed to update it.

my_dir="$(dirname "$0")"

printf Deleting old database and migrations info...
rm db.sqlite3
find . -path "$my_dir/../migrations/*.pyc"  -delete
find . -path "$my_dir/../migrations/*.py" -not -name "__init__.py" -delete

echo Deleted

echo Recreating the database...
$my_dir/setup_db.sh
echo Database recreated successfully
