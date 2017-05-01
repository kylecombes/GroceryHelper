from update_db import StoreDbUpdater
print('Downloading stores in Boston area...')
StoreDbUpdater(2000, 3000, 100)
print('Done downloading stores\n')

print('Importing grocery UPC data...')
import food_db_import
print('Done importing grocery UPC data')
print('App is ready to use')