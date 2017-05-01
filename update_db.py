"""
    Goes through all of the ZIP codes in the US,
    requests stores for the, and saves the result
    to the database.
"""

from store_fetcher import StoreFetcher
from database import StoreInfoAccessor, LocationInfoAccessor, DatabaseCreator
import math
import threading
import time
import argparse
from flask import Flask
from import_keys import *

app = Flask(__name__)

LOWEST_ZIP = 501
HIGHEST_ZIP = 99950
DEFAULT_WORKERS = 100


class StoreDbUpdater:

    def __init__(self, start_zip, end_zip, worker_count):

        with app.app_context():
            # Create a database if one does not already exist
            if not os.path.exists(StoreInfoAccessor.DATABASE_PATH):
                dc = DatabaseCreator()
                dc.init_db()

            start_time = time.time()

            # Break up ZIP codes
            zip_range = end_zip - start_zip + 1
            zips_per_worker = math.ceil(zip_range / worker_count)

            # Initialize API interface and data structure to store results in
            sf = StoreFetcher(SUPERMARKET_API_KEY)
            sd = StoresDS()

            # Start threads to parallelize downloads
            for i in range(worker_count):
                # Determine range
                w_start = start_zip + i*zips_per_worker
                w_end = w_start + zips_per_worker
                if w_end > end_zip:
                    w_end = end_zip
                # Create thread
                t_name = 'Thread {0: >2} (ZIPs {1:05}-{2:05})'.format(i, w_start, w_end)
                t = threading.Thread(target=self.__download_stores_in_range, name=t_name, args=(w_start, w_end, sf, sd))
                t.start()

            # Wait till all threads finish before continuing
            main_thread = threading.current_thread()
            for t in threading.enumerate():
                if t is not main_thread:
                    t.join()

            # Calculate how long it took to download (in seconds)
            dl_duration = time.time() - start_time
            # Print out results
            print("Downloaded data for {0} stores in {1:0.3f}s".format(len(sd.stores_dict), dl_duration))
            print("Average speed (using {0} threads): {1:0.3f} ms/request".format(worker_count, dl_duration/(end_zip-start_zip)/1000))

            # Save the data
            print('Saving data...')
            start_time = time.time()

            sia = StoreInfoAccessor()
            lia = LocationInfoAccessor(sia.db)
            for store in sd.stores_dict.values():
                # print(store)
                lia.save_location(store.location)
                store.location_id = store.location.id
                sia.save_store(store)
                # Update the store ID reference
                # print('Store ID: {}'.format(store.location.store_id))

                store.location.store_id = store.id
                lia.save_location(store.location)

            # Calculate how long it took to run (in seconds)
            save_duration = time.time() - start_time
            # Print out results
            print("Saved in {0:0.3f}s".format(save_duration))

    @staticmethod
    def __download_stores_in_range(start_zip, end_zip, fetcher, store_ds):
        """ Downloads all stores in a given range of ZIP codes.

            :param start_zip: the starting ZIP code - int
            :param end_zip: the ending ZIP code - int
            :param fetcher: a StoreFetcher to use to query for store data - StoreFetcher
            :param store_ds: the data structure holding all the stores downloaded - StoreDS
        """
        thread_name = threading.current_thread().getName()
        for zipcode in range(start_zip, end_zip):
            new_stores = fetcher.fetch_all_stores_in_zip(zipcode)
            store_ds.add_stores(new_stores)
            print('{0} fetched {1} stores for ZIP code {2:05}'.format(thread_name, len(new_stores), zipcode))

        # print('Fetched data for {0:01d} stores'.format(len(sd.stores_dict)))


class StoresDS:

    def __init__(self):
        self.stores_dict = {}
        self.lock = threading.Lock()

    def add_store(self, store):
        """ Adds a store if it is new, or updates a store if it already exists

            :param store: the store to add - Store
        """
        # Acquire a lock on this object so other threads can't modify it
        # (could be unnecessary given dictionaries are thread-safe).
        self.lock.acquire()
        try:
            old_store = self.stores_dict.get(store.store_id, None)
            if not old_store:
                # Add any new values previously empty and update any existing values
                #     old_store.merge(store)
                # else:
                self.stores_dict[store.store_id] = store
        finally:
            self.lock.release()


    def add_stores(self, stores):
        """ Adds multiple stores to the data set. Just a masked call to add_store, so same add/update behavior.

            :param stores: stores to add to the data set - list<Store>
        """
        for store in stores:
            self.add_store(store)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Define the named (optional) arguments that can be used when running this command
    parser.add_argument(
        '-s',
        '--start-zip',
        action='store',
        dest='start_zip',
        default=2000,
        type=int,
    )
    parser.add_argument(
        '-e',
        '--end-zip',
        action='store',
        dest='end_zip',
        default=3000,
        type=int,
    )
    parser.add_argument(
        '-w',
        '--workers',
        action='store',
        dest='workers',
        default=DEFAULT_WORKERS,
        type=int,
    )

    args = parser.parse_args()
    sdu = StoreDbUpdater(args.start_zip, args.end_zip, args.workers)
