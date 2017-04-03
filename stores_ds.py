import threading


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
