import datetime
from django.db import models 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import *
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import *

"""
Models:
1. Account
2. Item
3. Location
4. ItemLocation
5. Sale
6. ItemSale
7. Supplier
8. Customer
9. Transfer
10. ItemTransfer
11. Arrival
12. ItemArrival

Real world cases on how the quantity of an item in a specific location changes 
Case 1: 
	- Stocks of a specific item is transferred to another location - Item quantity on source location decreases, while the item quantity on the destination location increases - 
	- Note, if the item is depleted in destination or still haven't been to the destination, 
	a new instance of that ItemLocation is created...

Case 2: Stocks of the item are sold - Item quantity in the store decreases... 

Case 3: New stocks of the item have arrived - Item quantity in the warehouse (default location of arrival is at warehouse...) increases...

Todo: Initialize database with two default locations - Warehouse, and Branch Name (Add ability to change branch name), 
"""

class Account(models.Model):
	user = models.ForeignKey(User)
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')

	def __unicode__(self):
		return u'Profile of user: %s' %self.user.username


class WarningItems(models.Model):
	below_min = models.IntegerField(default=0)

	def __unicode__(self):
		return below_min


class Location (models.Model):
	name = models.CharField(max_length = 50, null = True)
	address = models.CharField(max_length = 200, null = True)
	user = models.ForeignKey(User, null=True)

	def __unicode__(self):
		return self.name

class ItemLocation(models.Model):
	item = models.ForeignKey('Item')
	location = models.ForeignKey(Location)
	current_stock = models.IntegerField(default = 0)
	re_order_point = models.PositiveIntegerField(default = 0)
	re_order_amount = models.PositiveIntegerField(default = 0)
		
	def __unicode__(self):
		return '%s' % (self.item)

class Supplier(models.Model):
	""" Suppliers can be also be paying users """
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	user = models.ForeignKey(User, null=True)

	def __unicode__(self):
		return self.name

class Customer(models.Model):
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	user = models.ForeignKey(User, null=True)

	def __unicode__(self):
		return self.name

class Item(models.Model):
	is_active = models.BooleanField(default=True)		# Active or Inactive
	name = models.CharField(max_length=70, null=True)
	description = models.CharField(max_length = 50, null=True)
	category = models.CharField(max_length = 50, null=True)
	brand = models.CharField(max_length = 50, null=True)
	model = models.CharField(max_length = 50, null=True)
	item_code = models.CharField(max_length = 50, unique = True)
	unit_cost = models.DecimalField(default = 0, max_digits = 100, decimal_places = 2)	
	date = models.DateTimeField(default=timezone.now)

	supplier = models.ForeignKey(Supplier, blank=True, null=True)
	location = models.ManyToManyField(Location, through='ItemLocation')
	user = models.ForeignKey(User, blank=False, null=True)

	def __unicode__(self):
		return " ".join((
            unicode(self.item_code),
            unicode(self.name),
            unicode(self.category),
            unicode(self.brand),
            unicode(self.model)
        ))

	@staticmethod
	def get_total_current_stock():
		items = Item.objects.all().prefetch_related('location')

		total = 0
		for item in items:
			item_location = item.itemlocation_set.all()
			for i in item_location:
				total = total + i.current_stock
		return total
	
	@staticmethod
	def get_total_stock_value():
		items = Item.objects.all()

		total = 0
		for item in items:
			item_location = item.itemlocation_set.all()
			for i in item_location:
				total = total + (i.current_stock * item.unit_cost) 
		return total

class Sale(models.Model):
	date = models.DateField(default=timezone.now)
	items = models.ManyToManyField(Item, through='ItemSale')
	customer = models.ForeignKey(Customer, null=True, blank=False)
	location = models.ForeignKey(Location, null=True, blank=False)
	user = models.ForeignKey(User, null=True, blank=False)

	def __unicode__(self):
		return ' '.join(unicode(self.date))

	def items_list(self):
		return ', '.join([sale.item for i in self.items.all()])

	@property
	def get_grand_total(self):
		grand_total = 0
		items_set = self.itemsale_set.all()
		for item in items_set: 
			grand_total = grand_total + item.total_cost
		return grand_total

class ItemSale(models.Model):
	is_active = models.BooleanField(default=True)
	item = models.ForeignKey(Item, blank=False)
	sale = models.ForeignKey(Sale)
	quantity = models.IntegerField(default = 0, null=True)

	def __unicode__(self):
		return self.item.__unicode__()

	@property
	def total_cost(self):
		total = self.item.unit_cost * self.quantity
		return total


class Transfer(models.Model):
	From = models.ForeignKey(Location, related_name = 'from+')
	To = models.ForeignKey(Location, related_name = 'to+')
	date = models.DateField(default=timezone.now)
	items = models.ManyToManyField(Item , through = 'ItemTransfer')
	user = models.ForeignKey(User)

	def __unicode__(self):
		return str(self.items)

class ItemTransfer(models.Model):
	quantity = models.IntegerField(default = 0)
	item = models.ForeignKey(Item)
	transfer = models.ForeignKey(Transfer)

	def __unicode__(self):
		return str(self.item.item_code)

class Arrival(models.Model):
	date = models.DateField(default=timezone.now)
	delivery_receipt_no = models.CharField(max_length=100, null=True, blank=False)
	tracking_no = models.CharField(max_length=100, null=True, blank=False)
	items = models.ManyToManyField(Item, through='ItemArrival')
	supplier = models.ForeignKey(Supplier)
	location = models.ForeignKey(Location)
	#user = models.ForeignKey(User, null=True)

	def __unicode__(self):
		return self.tracking_no

	def items_list(self):
		return ', '.join([a.item for i in self.items.all()])

	@staticmethod
	def apply_filter(start, end, supplier):
		items = Arrival.objects.filter(supplier=supplier).filter(date__gt=start, date__lt=end)
		return item

	@property
	def get_grand_total(self):
		grand_total = 0
		items_set = self.itemarrival_set.all()
		for item in items_set: 
			grand_total = grand_total + item.calculate_total
		return grand_total

class ItemArrival(models.Model):
	is_active = models.BooleanField(default=True)
	item = models.ForeignKey(Item)
	arrival = models.ForeignKey(Arrival)
	quantity = models.IntegerField()
	item_cost = models.FloatField(null=True, blank=True)

	def __unicode__(self):
		return " ".join((unicode(self.item.item_code),unicode(self.quantity)))

	@property
	def calculate_total(self):
		return self.item_cost * self.quantity

class Notifications(models.Model):
	below_min_date = models.DateTimeField(default=timezone.now())
	message = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True)
	item_loc = models.ForeignKey(ItemLocation)

	def __unicode__(self):
		return str(self.item_loc.item)

	def create(self, item_loc, message):
		item_loc = item_loc
		below_min_date = timezone.now()
		message = message


