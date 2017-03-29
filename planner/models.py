from django.db import models


# NOTE: To make parameters optional, set both 'blank' and 'null' to True.

class Location(models.Model):

    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)  # Could potentially be a territory
    zipcode = models.IntegerField()
    latitude = models.IntegerField(blank=True, null=True)
    longitude = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{0}, {1}, {2} {3:05d}'.format(self.street_address, self.city, self.state, self.zipcode)


class Store(models.Model):

    store_id = models.CharField(max_length=15)  # 'id' is already a built-in attribute
    name = models.CharField(max_length=60)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    #
    # def merge(self, new_store):
    #     """ Add data from another Store object. New attribute values are added and existing ones are updated, so long as
    #         the new values are not None or of length 0 (for strings). I.e. blank attributes on new_store are ignored.
    #
    #         :param new_store: a store to import values from - Store
    #     """
    #     if new_store.name and len(new_store.name) > 0:
    #         self.name = new_store.name
    #     if new_store.address and len(new_store.address) > 0:
    #         self.address = new_store.address
    #     if new_store.city and len(new_store.city) > 0:
    #         self.city = new_store.city
    #     if new_store.state and len(new_store.state) > 0:
    #         self.state = new_store.state
    #     if new_store.zip and new_store.zip > 0:
    #         self.zipcode = new_store.zip
    #     if new_store.phone and new_store.phone > 0:
    #         self.phone = new_store.phone

    def __str__(self):
        return '(ID: {0}) {1} at {2}'.format(self.store_id, self.name, self.location)


