from fetch_all import StoreFetcher
from stores_ds import StoresDS

lowest_zip = 501
highest_zip = 99950

if __name__ == '__main__':
    sf = StoreFetcher('5496fa4dc7')
    sd = StoresDS()
    for zipcode in range(lowest_zip+2, lowest_zip+31):
        new_stores = sf.fetch_all_stores_in_zip(zipcode)
        sd.add_stores(new_stores)
        print('Added %i stores for ZIP code %i' % (len(new_stores), zipcode))

    for store in sd.stores_dict.values():
        print(store)
