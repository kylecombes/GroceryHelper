from update_db import StoreDbUpdater
print('Downloading stores in Boston area...')
StoreDbUpdater(2000, 3000, 100)
print('Done downloading stores\n')

# TODO Check for UPC data file, download it and clean it if it doesn't exist
print('Checking for grocery UPC data...')
import os
if os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/Grocery_UPC_Database.csv')
print('Importing grocery UPC data...')
import food_csv_import
print('Done importing grocery UPC data')
print('App is ready to use')