import sqlite3
from flask import g
import os
from models import Store, Location, FoodItem


class DatabaseAccessor:

    FILENAME = 'grocery_db.sqlite'  # name of the sqlite database file
    DATABASE_PATH = '{}/{}'.format(os.path.dirname(os.path.realpath(__file__)), FILENAME)

    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            self.db = getattr(g, '_database', None)
            if self.db is None:
                self.db = g._database = sqlite3.connect(self.DATABASE_PATH)
            # Make the database query return a list of dictionaries rather than cursor rows
            self.db.row_factory = self.__make_dicts

    def _query_db(self, query, args=(), one=False):
        """ Queries (reads) the database.
            :param query: a SQL query statement (e.g. 'select * from stores') - string
            :param args: some SQL argument?
            :param one: if True, will return only the first result, otherwise all
            :return a tuple of dictionaries, where each element in the tuple represents a result in the database.
             The keys of the dictionaries correspond to the database column name and the values are the cell values.
        """
        cur = self.db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def _save(self, table_name, data, id=None):
        """ Saves data to the database, either by adding a new row (if id is None) or
            by updating an existing row (if is is not None).
            :param table_name: the table in the database to save the data to
            :param data: a dictionary where the keys correspond to the column names and the
             values correspond to the values to store in those cells
            :param id: the identifier of the row to update in the database
            :return the row id of the added new row, or 0 if an existing row was successfully updated
        """
        # Remove any items with a value of None
        cols = list(data.keys())
        vals = list(data.values())
        cols_clean = list()
        vals_sql = ''
        for i in range(len(cols)):
            val = vals[i]
            if val is not None:
                cols_clean.append(str(cols[i]))
                if isinstance(val, int):
                    vals_sql += '{},'.format(val)
                elif isinstance(val, str):
                    vals_sql += '"{}",'.format(val)
                else:
                    raise TypeError('Expected str or int, got {}.'.format(type(val)))
        # Create the SQL and execute it
        cols_sql = ','.join(cols_clean)
        cursor = self.db.cursor()
        if id:
            sql = "UPDATE {tn} SET ({cn})=({vals}) WHERE id=({id})". \
                format(tn=table_name, cn=cols_sql, vals=vals_sql[:-1], id=id)
            cursor.execute(sql, ())
        else:
            sql = "INSERT INTO {tn} ({cn}) VALUES ({vals})". \
                format(tn=table_name, cn=cols_sql, vals=vals_sql[:-1])
            row_id = cursor.execute(sql, ()).lastrowid

        self.db.commit()
        return row_id if row_id else 0

    # @app.teardown_appcontext
    def close(self):
        # self.db = getattr(g, '_database', None)
        if self.db is not None:
            self.db.close()

    @staticmethod
    def __make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))


class DatabaseCreator:

    SQL_CREATES = ['CREATE TABLE {} ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'store_id CHAR(15),'
                   'name CHAR(50),'
                   'location_id INT,'
                   'items CHAR(200));'.format(Store.DB_TABLE_NAME),

                   'CREATE TABLE {} ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'street_address CHAR(50),'
                   'city CHAR(20),'
                   'state CHAR(15),'
                   'zipcode INT,'
                   'latitude DOUBLE,'
                   'longitude DOUBLE,'
                   'store_id CHAR(15));'.format(Location.DB_TABLE_NAME),

                   'CREATE TABLE {} ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'item_id CHAR(15),'
                   'name CHAR(200),'
                   'aisle CHAR(15),'
                   'category CHAR(20),'
                   'description CHAR(100),'
                   'image_url CHAR(200));'.format(FoodItem.DB_TABLE_NAME)]

    def init_db(self):
        # Connecting to the database file
        conn = sqlite3.connect(DatabaseAccessor.DATABASE_PATH)
        c = conn.cursor()

        # Create new tables
        for sql in self.SQL_CREATES:
            c.execute(sql)

        # Committing changes and closing the connection to the database file
        conn.commit()
        conn.close()


class StoreInfoAccessor(DatabaseAccessor):
    def __init__(self, db=None):
        super().__init__(db)
        self.loc_info_accessor = LocationInfoAccessor(self.db)

    def get_all_stores(self):
        """ Gets all of the stores in the database
            :return a list of Store objects - [Store]
        """
        store_sql = 'SELECT * FROM {}'.format(Store.DB_TABLE_NAME)
        query_res = self._query_db(store_sql, ())
        res = list()
        for row in query_res:
            res.append(self.__parse_store(row))
        return res

    def get_stores_in_zip_range(self, start_zip, end_zip):
        """ Gets all the stores located in the given ZIP code range.
        :param start_zip: the starting ZIP code - int
        :param end_zip: the ending ZIP code (also searched) - int
        :return: a list of stores found in the given range - [Store]
        """
        locations = LocationInfoAccessor().get_locations_in_zip_range(start_zip, end_zip)
        res = list()
        for loc in locations:
            store_id = loc.store_id
            store = self.get_store(store_id)
            res.append(store)
        return res

    def get_store(self, store_id):
        """ Gets the information for one store.
        :param store_id: the store's alphanumeric ID
        :return: a Store object containing the store's information - Store
        """
        store_sql = 'SELECT * FROM {} WHERE id={}'.format(Store.DB_TABLE_NAME, store_id)
        query_res = self._query_db(store_sql, (), True)
        return self.__parse_store(query_res)

    def __parse_store(self, row):
        """ Internal method for parsing the results of a database query and saving it into a Store object """
        loc = self.loc_info_accessor.get_location(row['location_id'])
        store = Store(
            row['id'],
            row['store_id'],
            row['name'],
            loc
        )
        return store

    def save_store(self, store, location_info_accessor=None):
        if location_info_accessor:
            location_info_accessor.save_location(store.location)
        data = {
            'store_id': store.store_id,
            'name': store.name,
            'location_id': store.location.id,
        }
        new_id = self._save(store.DB_TABLE_NAME, data, store.id)
        # If we just added a store to the database, set the id attribute on the Store object
        if new_id:
            store.id = new_id
        return new_id


class LocationInfoAccessor(DatabaseAccessor):
    def __init__(self, db=None):
        super().__init__(db)

    def get_all_locations(self):
        """ Gets all of the locations stored in the database.
        :return: a Location object containing all the location's information - Location
        """
        location_sql = 'SELECT * FROM {}'.format(Location.DB_TABLE_NAME)
        query_res = self._query_db(location_sql, ())
        res = list()
        for row in query_res:
            res.append(self.__parse_location(row))
        return res

    def get_locations_in_zip_range(self, start_zip, end_zip):
        """ Gets the information for locations in ZIP codes in the given range.
        :param start_zip: the starting ZIP code - int
        :param end_zip: the ending ZIP code (also searched) - int
        :return: a list of Location objects in the given ZIP range - [Location]
        """
        sql = 'SELECT * FROM {} WHERE zipcode>={} AND zipcode<={}'.format(Location.DB_TABLE_NAME, start_zip, end_zip)
        query_res = self._query_db(sql, (), True)
        res = list()
        for row in query_res:
            res.append(self.__parse_location(row))
        return res

    def get_location(self, location_id):
        """ Gets the information for a location.
        :param location_id: the unique ID for the location - int
        :return: a Location object containing all the location's information - Location
        """
        sql = 'SELECT * FROM {} WHERE id={}'.format(Location.DB_TABLE_NAME, location_id)
        row = self._query_db(sql, (), True)
        return self.__parse_location(row)

    @staticmethod
    def __parse_location(row):
        """ Internal method for parsing the results of a database query and saving it into a Location object """
        loc = Location(
            row['id'],
            row['street_address'],
            row['city'],
            row['state'],
            row['zipcode'],
            row['latitude'],
            row['longitude']
        )
        return loc

    def save_location(self, location):
        data = {
            'street_address': location.street_address,
            'city': location.city,
            'state': location.state,
            'zipcode': location.zipcode,
            'latitude': location.latitude,
            'longitude': location.longitude,
        }
        new_row_id = self._save(location.DB_TABLE_NAME, data, location.id)
        if new_row_id:
            location.id = new_row_id
        return new_row_id
