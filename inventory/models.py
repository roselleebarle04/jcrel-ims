from django.db import models 
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone

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

	def get_absolute_url(self):
		return reverse('server_edit', kwargs={'pk': self.pk})


class Item(models.Model):
	status = models.CharField(max_length=50, null=True, default="INACTIVE") 		# Active or Inactive
	types = models.CharField(max_length = 50, null=True)
	category = models.CharField(max_length = 50, null=True)
	brand = models.CharField(max_length = 50, null=True)
	model = models.CharField(max_length = 50, null=True)
	supplier = models.ForeignKey("Supplier", blank=True, null=True, on_delete=models.SET_NULL)
	supplier_code = models.CharField(max_length = 50, unique = True)
	store_code = models.CharField(max_length = 50, unique = True)
	store_quantity = models.PositiveSmallIntegerField(default = 0)
	warehouse_quantity = models.PositiveSmallIntegerField(default = 0)
	unit_cost = models.DecimalField( default = 0, max_digits = 100, decimal_places = 2)
	srp = models.DecimalField(default = 0, max_digits = 100, decimal_places = 2)	
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __unicode__(self):
		return self.store_code

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


class Sale(models.Model):
	item = models.ForeignKey(Item, blank=True, on_delete=models.DO_NOTHING)
	quantity = models.PositiveSmallIntegerField(default = 0)
	date = models.DateField(default=timezone.now)

	def __unicode__(self):
		return self.item.store_code

	@property	
	def calculate_cost(self):
		total = self.quantity * self.item.srp
		return total

	@property
	def total_quantity(self):
		qty = self.item.store_quantity + self.item.warehouse_quantity
		return qty
	


class AddArrival(models.Model):
	date = models.DateField(default=timezone.now)
	dr = models.PositiveSmallIntegerField(default=0)
	tracking_no = models.PositiveSmallIntegerField(default=0)
	supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.SET_NULL)
	itemName = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
	qty = models.PositiveSmallIntegerField(default=0)
	itemCost = models.FloatField(null=True, blank=True)
	
	# itemName = models.CharField(max_length=300, null=True)
	# qty = models.PositiveSmallIntegerField(default=0)
	# itemCost = models.FloatField(null=True, blank=True)
	# transfer_date = models.DateField(default=timezone.now)


class Transfer_item(models.Model):
	item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
	quantity_to_transfer = models.PositiveSmallIntegerField(default = 0)
	transfer_date = models.DateField(default=timezone.now)
