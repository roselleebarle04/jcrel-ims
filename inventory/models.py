from django.db import models
from django.core.urlresolvers import reverse

class AddArrival(models.Model):
	itemName = models.CharField(max_length=300, null=True)
	qty = models.PositiveSmallIntegerField(default=0)
	itemCost = models.FloatField(null=True, blank=True)

class Accounts(models.Model):
	#All signed up accounts will be saved here
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	password = models.CharField(max_length=50)


class Item(models.Model):
	store_code = models.CharField(max_length=200, null=True)	# Store Code
	supplier_code = models.CharField(max_length=200, null=True)	# Supplier Code
	status = models.CharField(max_length=50, null=True, default="INACTIVE") 		# Active or Inactive
	unit_cost = models.IntegerField(default=0)

	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	category = models.ForeignKey("Category", db_index=True, null=True)
	brand = models.ForeignKey("Brand", db_index=True, null=True)
	item_model = models.ForeignKey("ItemModel", db_index=True, null=True)
	supplier = models.ForeignKey("Supplier", db_index=True, null=True)

	class Meta:
		ordering = ('created',)

class Supplier(models.Model):
	""" Suppliers can be also be paying users """
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	# owner = models.ForeignKey("accounts.User")

class Category(models.Model):
	""" Categories describe an Item """
	description = models.CharField(max_length=100, null=True)

class Brand(models.Model):
	""" Brands describe an Item """
	description = models.CharField(max_length=100, null=True)

class ItemModel(models.Model):
	""" Models describe the model of a particular Item """
	description = models.CharField(max_length=100, null=True)

class Sale(models.Model):
	#code = models.ForeignKey(Item)
	item_code =  models.CharField(max_length = 6, null = False , blank = False)
	quantity = models.PositiveSmallIntegerField(default = 0)
	srp = models.DecimalField(max_digits = 10, decimal_places = 2)

class Transfer_item(models.Model):
	item_code =  models.CharField(max_length = 6, null = False , blank = False)
	quantity_to_transfer = models.PositiveSmallIntegerField(default = 0)
	transfer_date = models.DateTimeField(blank=True,null=True)