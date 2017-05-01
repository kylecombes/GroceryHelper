""" Imports the Grocery UPC Database (http://www.grocery.com/open-grocery-database-project/) into the database """
import csv
from database import FoodItemInfoAccessor
from models import FoodItem
from flask import Flask

app = Flask(__name__)

with app.app_context():

    fia = FoodItemInfoAccessor()

    line_count = 0

    with open('static/Grocery_UPC_Database.csv', newline='', encoding='utf-8') as csvfile:
        try:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                # if reader.line_num == 652:
                #     stop = True
                item_id = row[0]
                line_count += 1
                if reader.line_num == 1:
                    continue  # Skip the first row, which is column names
                # upc14 = row[1]
                upc12 = row[2]
                name = row[4].replace('"', '')
                item = FoodItem(item_id, name, None, None, None, None)
                fia.save_item(item)
        finally:
            print('Last row looked at:', line_count)
            fia.close()
            csvfile.close()
    print('Finished reading Grocery_UPC_Database.csv and saving its info to the database.')
