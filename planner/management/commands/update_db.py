from django.core.management.base import BaseCommand

from fetch_all import StoreFetcher
from keys import *
from stores_ds import StoresDS
import math
import threading
import time


class Command(BaseCommand):

    help = 'Goes through all of the ZIP codes in the US, requests stores for the, and saves the result.'

    LOWEST_ZIP = 501
    HIGHEST_ZIP = 99950
    DEFAULT_WORKERS = 30

    def add_arguments(self, parser):
        # Define the named (optional) arguments that can be used when running this command
        parser.add_argument(
            '-s',
            '--start-zip',
            action='store',
            dest='start-zip',
            default=self.LOWEST_ZIP,
            type=int,
        )
        parser.add_argument(
            '-e',
            '--end-zip',
            action='store',
            dest='end-zip',
            default=self.HIGHEST_ZIP,
            type=int,
        )
        parser.add_argument(
            '-w',
            '--workers',
            action='store',
            dest='workers',
            default=self.DEFAULT_WORKERS,
            type=int,
        )

    def handle(self, *args, **options):
        start_time = time.time()
        # Load any options passed to the command
        start_zip = options['start-zip']
        end_zip = options['end-zip']
        worker_count = options['workers']

        # Break up ZIP codes
        zip_range = end_zip - start_zip + 1
        zips_per_worker = math.ceil(zip_range / worker_count)

        # Initialize API interface and data structure to store results in
        sf = StoreFetcher(API_KEY)
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

        for store in sd.stores_dict.values():
            # print(store)
            store.location.save()
            store.location_id = store.location.id
            store.save()

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
        # 10505, 12000
        thread_name = threading.current_thread().getName()
        for zipcode in range(start_zip, end_zip):
            new_stores = fetcher.fetch_all_stores_in_zip(zipcode)
            store_ds.add_stores(new_stores)
            print('{0} added {1} stores for ZIP code {2:05}'.format(thread_name, len(new_stores), zipcode))

        # print('Fetched data for {0:01d} stores'.format(len(sd.stores_dict)))
