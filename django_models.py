
class Location:

    DB_TABLE = 'planner_location'

    def __init__(self, db=None, location_id=None):
        if location_id and db:
            sql_query = 'SELECT * FROM {} WHERE id={}'.format(self.DB_TABLE, location_id)
            query_res = db.query_db(sql_query, (), True)
            self.street_address = query_res['street_address']
            self.city = query_res['city']
            self.state = query_res['state']
            self.zipcode = query_res['zipcode']
            self.latitude = query_res['latitude']
            self.longitude = query_res['longitude']
        else:
            self.street_address = None
            self.city = None
            self.state = None
            self.zipcode = None
            self.latitude = None
            self.longitude = None

    def save_to_db(self, db):
        data = {
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'latitude': self.latitude,
            'longitude': self.longitude,
            }
        return db.save(self.DB_TABLE, data)



    def __str__(self):
        return '{0}, {1}, {2} {3:05d}'.format(self.street_address, self.city, self.state, self.zipcode)


# class Store(models.Model):
#
#     store_id = models.CharField(max_length=15)  # 'id' is already a built-in attribute
#     name = models.CharField(max_length=60)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     #
#     # def merge(self, new_store):
#     #     """ Add data from another Store object. New attribute values are added and existing ones are updated, so long as
#     #         the new values are not None or of length 0 (for strings). I.e. blank attributes on new_store are ignored.
#     #
#     #         :param new_store: a store to import values from - Store
#     #     """
#     #     if new_store.name and len(new_store.name) > 0:
#     #         self.name = new_store.name
#     #     if new_store.address and len(new_store.address) > 0:
#     #         self.address = new_store.address
#     #     if new_store.self.city and len(new_store.self.city) > 0:
#     #         self.city = new_store.self.city
#     #     if new_store.self.state and len(new_store.self.state) > 0:
#     #         self.state = new_store.self.state
#     #     if new_store.zip and new_store.zip > 0:
#     #         self.zipcode = new_store.zip
#     #     if new_store.phone and new_store.phone > 0:
#     #         self.phone = new_store.phone
#
#     def __str__(self):
#         return '(ID: {0}) {1} at {2}'.format(self.store_id, self.name, self.location)
#
#
# class FoodItem(models.Model):
#
#     aisle = models.CharField(max_length=30)
#     category = models.CharField(max_length=30)
#     description = models.CharField(max_length=300)
#     item_id = models.IntegerField()
#     image_url = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     # store = models.ForeignKey(Store, blank=True, null=True)
