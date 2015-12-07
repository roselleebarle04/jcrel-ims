from django.test import TestCase, Client, RequestFactory

from inventory.models import *
from inventory.forms import *
from inventory.reports import *

"""
TODO WHEN WRITING TESTS:
1. Change permissions for your user: ALTER ROLE jcrel CREATEDB;

Resources
https://docs.djangoproject.com/en/1.8/topics/testing/overview/
http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/
https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/

"""

class ItemTestCase(TestCase):
	# fixtures = ['inventory_views_testdata.json']

	def setUp(self):
		""" 
		The setUp function is run first everytime we start the test. It sets everything up!
		"""
		self.client = Client()
		self.create_test_data()

	def create_test_data(self): 
		self.supplier1 = Supplier.objects.create(name='JB', address='Cagayan', phone='221-0139')
		self.location1 = Location.objects.create(name='Warehouse', address='Brgy. San Miguel, Iligan City')
		
		self.item1 = Item.objects.create(is_active=True, category='Amplifier', brand='Boston', model='BP20', name='Item1', description='Insert long description here', item_code='S-1-5099', unit_cost='1000', created=timezone.now(), supplier=self.supplier1)

	def test_create_item(self):
		response = self.client.get('/items/')
		self.assertEqual(response.status_code, 200)

		item = Item.objects.get(item_code='S-1-5099')
		self.assertEqual(item, self.item1)
