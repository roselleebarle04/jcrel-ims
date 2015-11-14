from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AddArrival(models.Model):
	itemName = models.CharField(max_length=300, null=True)
	qty = models.PositiveSmallIntegerField(default=0)
	itemCost = models.FloatField(null=True, blank=True)

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
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	types = models.CharField(max_length = 50)
	category = models.CharField(max_length = 50)
	brand = models.CharField(max_length = 50)
	model = models.CharField(max_length = 50)
	supplier = models.ForeignKey("Supplier")
	supplier_code = models.CharField(max_length = 50)
	store_code = models.CharField(max_length = 6)
	store_quantity = models.PositiveSmallIntegerField(default = 0)
	warehouse_quantity = models.PositiveSmallIntegerField(default = 0)
	unit_cost = models.DecimalField( default = 0, max_digits = 100, decimal_places = 2)
	srp = models.DecimalField(default = 0, max_digits = 100, decimal_places = 2)

	def __unicode__(self):
		return self.store_code

	class Meta:
		ordering = ('created',)

class Supplier(models.Model):
	""" Suppliers can be also be paying users """
	name = models.CharField(max_length=200, null=True)
	address = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)

	# owner = models.ForeignKey("accounts.User")

class Sale(models.Model):
	item = models.ForeignKey(Item)
	supplier = models.ForeignKey(Supplier)
	quantity = models.PositiveSmallIntegerField(default = 0)

class Transfer_item(models.Model):
	item = models.ForeignKey(Item)
	quantity_to_transfer = models.PositiveSmallIntegerField(default = 0)
	transfer_date = models.DateTimeField(blank=True,null=True)
