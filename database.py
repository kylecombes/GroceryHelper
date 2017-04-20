import sqlite3
from flask import g
import os
from models import Store, Location


class DatabaseAccessor:

    DATABASE = os.path.dirname(os.path.realpath(__file__)) + '/db.sqlite3'

    def __init__(self, db=None):
        if db:
            self.db = db
        else:
            self.db = getattr(g, '_database', None)
            if self.db is None:
                self.db = g._database = sqlite3.connect(self.DATABASE)
            # Make the database query return a list of dictionaries rather than cursor rows
            self.db.row_factory = self.make_dicts


    def query_db(self, query, args=(), one=False):
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


    def save(self, table_name, data, id=None):
        """ Saves data to the database, either by adding a new row (if id is None) or
            by updating an existing row (if is is not None).
            :param table_name: the table in the database to save the data to
            :param data: a dictionary where the keys correspond to the column names and the
             values correspond to the values to store in those cells
            :param id: the identifier of the row to update in the database
            :return the row id of the added new row, or 0 if an existing row was successfully updated
        """
        col_sql = ','.join(list(data.keys()))
        val_sql = ','.join(list(data.values()))
        if id:
            sql = "UPDATE {tn} SET ({cn})=({vals}) WHERE {idf}=({id})".\
                format(tn=table_name, cn=col_sql, vals=val_sql, id=id)
            self.db.execute(sql, ())
        else:
            sql = "INSERT INTO {tn} ({cn}) VALUES ({vals})".\
                format(tn=table_name, cn=col_sql, vals=val_sql)
            new_row_id = self.db.execute(sql, ())
            return new_row_id

        return 0


    # @app.teardown_appcontext
    def close(self):
        # self.db = getattr(g, '_database', None)
        if self.db is not None:
            self.db.close()

    @staticmethod
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))


class DatabaseCreator:

    @staticmethod
    def init_db(app, db):
        with app.app_context():
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()


class StoreInfoAccessor(DatabaseAccessor):

    def __init__(self, db=None):
        super().__init__(db)

    def get_all_stores(self):
        store_sql = 'SELECT * FROM {}'.format(Store.DB_TABLE_NAME)
        location_sql = 'SELECT * FROM {} WHERE id={}'
        query_res = self.query_db(store_sql, ())
        res = list()
        loc_info_accessor = LocationInfoAccessor(self.db)
        for row in query_res:
            loc = loc_info_accessor.get_location(row['location_id'])
            store = Store(
                row['store_id'],
                row['name'],
                loc
            )
            res.append(store)
        return res


class LocationInfoAccessor(DatabaseAccessor):

    def __init__(self, db=None):
        super().__init__(db)

    def get_location(self, location_id):
        sql = 'SELECT * FROM {} WHERE id={}'.format(Location.DB_TABLE_NAME, location_id)
        row = self.query_db(sql, (), True)
        loc = Location(
            row['street_address'],
            row['city'],
            row['state'],
            row['zipcode'],
            row['latitude'],
            row['longitude']
        )
        return loc

    def get_all_locations(self):
        location_sql = 'SELECT * FROM {}'.format(Location.DB_TABLE_NAME)
        query_res = self.query_db(location_sql, ())
        res = list()
        for row in query_res:
            loc = Location(
                row['street_address'],
                row['city'],
                row['state'],
                row['zipcode'],
                row['latitude'],
                row['longitude']
            )
            res.append(loc)
        return res
