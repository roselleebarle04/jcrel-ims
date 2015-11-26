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

        # Create new sale
        sale1 = Sale(date=timezone.now())
        sale1.save()

        # Now add items to the sale
        sale_item1 = SoldItem(item=item1, sale=sale1, quantity=100)
        sale_item1.save()

        # Create new arrival
        arrival1 = Arrival(delivery_receipt_no='DR-123', tracking_no='TR-123', supplier=supplier1)
        arrival1.save()

        # Add items to the arrival
        arrival_item1 = ArrivedItem(item=item1, arrival=arrival1,quantity=100,item_cost=100.1)
        arrival_item1.save()

    def handle(self, *args, **options):
        self._create_data()