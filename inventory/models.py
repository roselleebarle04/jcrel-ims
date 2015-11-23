from django.db import models 
from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import *
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

#TRIGGER

class Account(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	password = models.CharField(max_length=50)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.last_name


class Item(models.Model):
	status = models.BooleanField(default=True)		# Active or Inactive
	types = models.CharField(max_length = 50, null=True)
	category = models.CharField(max_length = 50, null=True)
	brand = models.CharField(max_length = 50, null=True)
	model = models.CharField(max_length = 50, null=True)
	supplier = models.ForeignKey("Supplier", blank=True, null=True, on_delete=models.SET_NULL)
	item_code = models.CharField(max_length = 50, unique = True)
	store_quantity = models.PositiveSmallIntegerField(default = 0)
	warehouse_quantity = models.PositiveSmallIntegerField(default = 0)
	srp = models.DecimalField(default = 0, max_digits = 100, decimal_places = 2)	
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return " ".join((
            unicode(self.item_code),
            unicode(self.types),
            unicode(self.category),
            unicode(self.brand),
            unicode(self.model)
        ))

	@property
	def total_quantity(self):
		qty = self.store_quantity + self.warehouse_quantity
		return qty	

	class Meta:
		ordering = ('created',)
	

class Supplier(models.Model):
	""" Suppliers can be also be paying users """
	avatar = models.ImageField('avatar', upload_to='avatar', null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return self.name

class Customer(models.Model):
	avatar = models.ImageField('avatar', upload_to='avatar', null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return self.name


class Sale(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.PositiveSmallIntegerField(default = 0)
	date = models.DateField(default=timezone.now)

	def __unicode__(self):
		return " ".join((unicode(self.date)))
	
	@property	
	def calculate_cost(self):
		total = self.quantity * self.item_cost
		return total
	
class Sales_history(models.Model):
	sale = models.ForeignKey(Sale)
	

# class Arrival(models.Model):
# 	"""	This model refers to the arrival of the store owner from its suppliers """
# 	date = models.DateField(default=timezone.now)
# 	dr = models.CharField(max_length=100, null=True, blank=True)
# 	trckng_no = models.CharField(max_length=100, null=True, blank=True)
# 	supp = models.ForeignKey(Supplier)
# 	arrival_items = models.ManyToManyField(Item, through='ArrivedItem')
	
# 	def __unicode__(self):
# 		return self.dr

# class ArrivedItem(models.Model):
# 	arrival = models.ForeignKey(Arrival)
# 	arrived_item = models.ForeignKey(Item)
# 	arrived_quantity = models.PositiveIntegerField(default=0)
# 	itemCost = models.FloatField(null=True, blank=True)


class Location (models.Model):
	branch_name = models.CharField(max_length = 50, null = True)
	address = models.CharField(max_length = 200, null = True)

	def __unicode__(self):
		return self.branch_name


class Transfer (models.Model):
	transfer_date = models.DateField(default=timezone.now)
	location = models.ForeignKey(Location)
	trans_item = models.ManyToManyField(Item, through = 'Transfer_item')

	def __unicode__(self):
		return '%s' %(self.location)

class Transfer_item(models.Model):
	item = models.ForeignKey(Item)
	trans = models.ForeignKey(Transfer)
	quantity_to_transfer = models.PositiveSmallIntegerField(default = 0)
	
	def __unicode__(self):
		return self.item.item_code


class Arrival(models.Model):
	"""	This model refers to the arrival of the store owner from its suppliers """
	date = models.DateField(default=timezone.now)
	delivery_receipt_no = models.CharField(max_length=100, null=True, blank=True)
	tracking_no = models.CharField(max_length=100, null=True, blank=True)
	items = models.ManyToManyField(Item, through='ArrivedItem')
	supplier = models.ForeignKey(Supplier)

	def __unicode__(self):
		return self.tracking_no

	# def items_list(self):
	# 	return ', '.join([a.item for i in self.items.all()])

class ArrivedItem(models.Model):
	item = models.ForeignKey(Item)
	arrival = models.ForeignKey(Arrival)
	quantity = models.IntegerField(default=0)
	item_cost = models.FloatField(null=True, blank=True)

	#source_location = models.ForeignKey(Location)
	#destination = models.ForeignKey(Location)
	def __unicode__(self):
		return self.item.item_code
