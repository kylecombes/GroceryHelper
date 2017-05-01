""" Imports the Grocery UPC Database (http://www.grocery.com/open-grocery-database-project/) into the database """
# import csv
import xlrd
import os
from database import FoodItemInfoAccessor
from models import FoodItem
from flask import Flask

app = Flask(__name__)

UPC_XLSX_NAME = 'Grocery_UPC_Database.xlsx'

with app.app_context():

    fia = FoodItemInfoAccessor()

    # line_count = 0

    # Check for UPC data file, download it if it doesn't exist
    print('Checking for grocery UPC data...')
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/' + UPC_XLSX_NAME):
        print('Downloading grocery UPC database...')
        import urllib.request

        urllib.request.urlretrieve('http://www.grocery.com/download-file/19054', UPC_XLSX_NAME)
        print('Finished downloading.')
    else:
        print('Grocery UPC database already downloaded.')

    print('Opening the data file...')
    # Import the data from the spreadsheet
    book = xlrd.open_workbook(UPC_XLSX_NAME)

    sheet = book.sheets()[0]

    print('Importing the data...')
    for r in range(1, sheet.nrows):  # Skip the first row, as it's just column names
        # row = sheet.row(r)
        item_id = int(sheet.cell(r, 0).value)
        upc12 = int(sheet.cell(r, 2).value)
        name = sheet.cell(r, 4).value.replace('"', '')
        item = FoodItem(item_id, name, None, None, None, None)
        fia.save_item(item)
        if r % 100 == 0:
            print('Successfully saved row', r)
    print('Grocery UPC data successfully imported.')

    # CSV method:
    # with open('static/Grocery_UPC_Database.csv', newline='', encoding='utf-8') as csvfile:
    #     try:
    #         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #         for row in reader:
    #             # if reader.line_num == 652:
    #             #     stop = True
    #             item_id = row[0]
    #             line_count += 1
    #             if reader.line_num == 1:
    #                 continue  # Skip the first row, which is column names
    #             # upc14 = row[1]
    #             upc12 = row[2]
    #             name = row[4].replace('"', '')
    #             item = FoodItem(item_id, name, None, None, None, None)
    #             fia.save_item(item)
    #     finally:
    #         print('Last row looked at:', line_count)
    #         fia.close()
    #         csvfile.close()
    # print('Finished reading Grocery_UPC_Database.csv and saving its info to the database.')

