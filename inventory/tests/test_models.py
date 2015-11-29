from django.test import TestCase, Client, RequestFactory

from inventory.models import *
from inventory.forms import *
from inventory.reports import *

# Things to remember when writing tests: 
# 1. When you create a new tests folder, make sure to include __init__.py inside it (ALWAYS DO WHEN YOU CREATE NEW DIRS)
# 2. ALTER ROLE jcrel CREATEDB; - Grant write access to your db user

# class AnimalTestCase(TestCase):
# 	def setUp(self):
# 		Animal.objects.create(name="lion", sound="roar")
	
# 	def test_animals_can_speak(self):
# 		lion = Animal.objects.get(name="lion")
# 		self.assertEqual(lion.speak(), 'The Lion says roar')


class ItemTestCase(TestCase):
	def setUp(self):
		self.clent = Client()
		Supplier.objects.create(name='JB', address='Cagayan', phone='221-0139')
        Customer.objects.create(name='Roselle Ebarle', address='Iligan City', phone='09462240166')

        supplier1 = Supplier.objects.get(name='JB')
    	Item.objects.create(category='Amplifier', brand='Boston', model='BP20', supplier=supplier1, item_code='S-1-5099', store_quantity=100, warehouse_quantity=100, srp=1500, created=timezone.now())
    	Location.objects.create(branch_name='BR1', address='Brgy. San Miguel, Iligan City')

        # sale1 = Sale(date=timezone.now())
        # sale_item1 = SoldItem(item=item1, sale=sale1, quantity=100)
        # arrival1 = Arrival(delivery_receipt_no='DR-123', tracking_no='TR-123', supplier=supplier1)
        # arrival_item1 = ArrivedItem(item=item1, arrival=arrival1,quantity=100,item_cost=100.1)

	def test_create_item(self):
		response = self.client.get('/items/')
		self.assertEqual(response.status_code, 200)

		item = Item.objects.get(item_code='S-1-409')
		self.assertEqual(item.category, 'Amplifiers')
		self.assertNotEqual(0,1)
