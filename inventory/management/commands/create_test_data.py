from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import *

class Command(BaseCommand):
    # args = '<foo bar ...>'
    # help = 'our help string comes here'

    def _create_data(self):
    	supplier1 = Supplier(name='JB', address='Cagayan', phone='221-0139')
    	supplier1.save()

    	item1 = Item(category='Amplifier', brand='Boston', model='BP20', supplier=supplier1, supplier_code='E-1-408', store_code='S-1-409', store_quantity=100, warehouse_quantity=100, unit_cost=1000, srp=1500, created=timezone.now())
    	item1.save()

    	sales1 = Sale(item=item1, quantity=5)
    	sales1.save()

    	arrival1 = AddArrival(dr=1, tracking_no=1, supplier=supplier1, itemName=item1, qty=100, itemCost=980)
    	arrival1.save()

    	transfer1 = Transfer_item(item=item1, quantity_to_transfer=50)
    	transfer1.save()
    def handle(self, *args, **options):
        self._create_data()