from django.db import models


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





"""
from django.db import models

class Item(models.Model):
	category = models.CharField(max_length=200, null=True)
	itemType = models.CharField(max_length=200, null=True)
	
	itemCode = models.CharField(max_length=200, null=True)
	supplierCode = models.CharField(max_length=200, null=True)
	minimumRequired = models.IntegerField(default=0)
	store_quantity = models.IntegerField(default=0)
	warehouse_quantity = models.IntegerField(default=0)
	unit_cost = models.BigIntegerField(default=0)
	supplier = models.ForeignKey("dashboard.Supplier", db_index=True, null=True)

	def __unicode__(self):
		return "%s | %s | %s | %s" % (self.category, self.itemType, self.itemModel, self.brand)

	@staticmethod
	def get_inventory_balance():
		total_item_cost = 0
		item_list = Item.objects.all()
		for item in item_list: 
			total_item_cost += item.unit_cost * (item.store_quantity + item.warehouse_quantity) 
		return total_item_cost

class Arrival(models.Model):
	item = models.ForeignKey("dashboard.Item", db_index=True, null=True, blank=True)
	date = models.DateField(auto_now=True, null=True)
	tracking_number = models.CharField(max_length=200, null=True)
	delivery_receipt = models.CharField(max_length=200, null=True)
	quantity = models.IntegerField(default=0)

class Sale(models.Model):
	item = models.ForeignKey("dashboard.Item", db_index=True, null=True, blank=True)
	quantity = models.IntegerField(default=0)
	date = models.DateField(auto_now=True, null=True)

	@property
	def total_cost(self):
		return self.quantity * self.item.unit_cost

	@staticmethod
	def grand_total():
		grand_total = 0
		all_sales = Sale.objects.all()
		for sale in all_sales: 
			grand_total += sale.total_cost
		return grand_total

class Transfer(models.Model):
	item = models.ForeignKey("dashboard.Item", db_index=True, null=True, blank=True)
	quantity = models.IntegerField(default=0)
	date = models.DateField(auto_now=True, null=True)
	location_to = models.CharField(max_length=200, null=True)
	location_from = models.CharField(max_length=200, null=True)

class Supplier(models.Model):
	description = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return self.description

"""