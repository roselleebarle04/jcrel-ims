from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import *

class Command(BaseCommand):
    def _create_data(self):
    	supplier1 = Supplier(name='JB', address='Cagayan', phone='221-0139')
    	supplier1.save()

        customer1 = Customer(name='Roselle Ebarle', address='Iligan City', phone='09462240166')
        customer1.save()

    	item1 = Item(category='Amplifier', brand='Boston', model='BP20', supplier=supplier1, item_code='S-1-409', store_quantity=100, warehouse_quantity=100, srp=1500, created=timezone.now())
    	item1.save()

    	location1 = Location(branch_name='BR1', address='Brgy. San Miguel, Iligan City')
    	location1.save()

    def handle(self, *args, **options):
        self._create_data()