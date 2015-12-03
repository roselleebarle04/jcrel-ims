from django.db import models 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import *
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class Account(models.Model):
	user = models.ForeignKey(User)
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')

	def __unicode__(self):
		return u'Profile of user: %s' %self.user.username


class Location (models.Model):
	branch_name = models.CharField(max_length = 50, null = True)
	address = models.CharField(max_length = 200, null = True)

	def __unicode__(self):
		return self.branch_name

class WarningItems(models.Model):
	below_min = models.IntegerField(default=0)

	def __unicode__(self):
		return below_min


class ItemLocation(models.Model):
	destination = models.ForeignKey(Location)
	quantity = models.PositiveSmallIntegerField(default = 0)
	item = models.ForeignKey('Item' ,blank = True)
	
	def __unicode__(self):
		return '%s' %(self.destination)


class Item(models.Model):
	status = models.BooleanField(default=True)		# Active or Inactive
	types = models.CharField(max_length = 50, null=True)
	category = models.CharField(max_length = 50, null=True)
	brand = models.CharField(max_length = 50, null=True)
	model = models.CharField(max_length = 50, null=True)
	supplier = models.ForeignKey("Supplier", blank=True, null=True, on_delete=models.SET_NULL)
	item_code = models.CharField(max_length = 50, unique = True)
	location = models.ManyToManyField(Location, through = 'ItemLocation' )
	srp = models.DecimalField(default = 0, max_digits = 100, decimal_places = 2)	
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	# below_min = models.IntegerField(default=0)
	
		
	def __unicode__(self):
		return " ".join((
            unicode(self.item_code),
            unicode(self.types),
            unicode(self.category),
            unicode(self.brand),
            unicode(self.model)
        ))

	def get_description(self):
		return self.category + ' ' + self.brand + ' ' + self.model


	class Meta:
		ordering = ('created',)



class AddItem(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.PositiveSmallIntegerField(default = 0)
	loc = models.ForeignKey(ItemLocation)
	def __unicode__(self):
		return self.item.item_code


class Supplier(models.Model):
	""" Suppliers can be also be paying users """
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return self.name

class Customer(models.Model):
	avatar = models.ImageField('avatar', upload_to='avatar', default='img/avatar.jpeg')
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return self.name

class Sale(models.Model):
	date = models.DateField(default=timezone.now)
	items = models.ManyToManyField(Item, through='SoldItem')

	def __unicode__(self):
		return ' '.join(unicode(self.date))

	def items_list(self):
		return ', '.join([a.item for i in self.items.all()])

	def get_grand_total(self):
		grand_total = 0
		items_set = self.solditem_set.all()
		for item in items_set: 
			grand_total = grand_total + item.total_cost()
		return grand_total

class SoldItem(models.Model):
	is_active = models.BooleanField(default=True)
	item = models.ForeignKey(Item, blank=False)
	sale = models.ForeignKey(Sale)
	quantity = models.PositiveSmallIntegerField(default = 0, null=True)

	def __unicode__(self):
		return self.item.__unicode__()

		
	def total_cost(self):
		total = self.item.srp * self.quantity
		return total


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

	def items_list(self):
		return ', '.join([a.item for i in self.items.all()])

	@staticmethod
	def apply_filter(start, end, supplier):
		items = Arrival.objects.filter(supplier=supplier).filter(date__gt=start, date__lt=end)
		return items

	def get_grand_total(self):
		grand_total = 0
		items_set = self.arriveditem_set.all()
		for item in items_set: 
			grand_total = grand_total + item.calculate_total()
		return grand_total

class ArrivedItem(models.Model):
	is_active = models.BooleanField(default=True)
	item = models.ForeignKey(Item)
	arrival = models.ForeignKey(Arrival)
	quantity = models.IntegerField()
	item_cost = models.FloatField(null=True, blank=True)

	
	def __unicode__(self):
		return " ".join((unicode(self.item.item_code),unicode(self.quantity)))
		
	def calculate_total(self):
		return self.item_cost * self.quantity


