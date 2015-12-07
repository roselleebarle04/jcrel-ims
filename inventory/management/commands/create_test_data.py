from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import *

class Command(BaseCommand):
    # def _initialize_db(self):
    #     # First, let's initialize db with the DEFAULT locations
    #     location_warehouse = Location.objects.create(name='Warehouse', address='Brgy. San Miguel, Iligan City')
    #     location_store = Location.objects.create(name='Store', address='Tambo Hinaplanon, Iligan City')

    #     # Register a supplier
    #     supplier1 = Supplier.objects.create(name='JB', address='Cagayan', phone='221-0139')

    #     # Register an initial item
    #     item1 = Item.objects.create(category='Amplifier', brand='Boston', model='BP20', supplier=supplier1, item_code='S-1-409', srp=1500, created=timezone.now())
        
    #     # Add the quantity of the item in the default location
    #     item1_quantity = ItemLocation.objects.create(item=item1,location=location_warehouse,quantity=100)

    def _create_data(self):
    	supplier1 = Supplier(name='JB', address='Cagayan', phone='221-0139')
    	supplier1.save()

        customer1 = Customer(name='Roselle Ebarle', address='Iligan City', phone='09462240166')
        customer1.save()

    	item1 = Item(name='Item1', description='Insert long desc. here', category='Amplifier', brand='Boston', model='BP20', item_code='S-1-409', unit_cost=1000, date=timezone.now(), supplier=supplier1)
    	item1.save()

    	location1 = Location(branch_name='BR1', address='Brgy. San Miguel, Iligan City')
    	location1.save()

        itemLocation1 = ItemLocation(item=item1, location=location1, current_stock=100, re_order_point=5, re_order_amount=100)
        itemLocation1.save()

        # Create new sale
        sale1 = Sale(customer=customer1, location=location1, date=timezone.now())
        sale1.save()

        # Now add items to the sale
        itemSale1 = ItemSale(item=item1, sale=sale1, quantity=100)
        itemSale1.save()

        # Create new arrival
        arrival1 = Arrival(delivery_receipt_no='DR-123', tracking_no='TR-123', supplier=supplier1)
        arrival1.save()

        # Add items to the arrival
        itemArrival1 = ItemArrival(item=item1, arrival=arrival1,quantity=100,item_cost=100.1)
        itemArrival1.save()

    def handle(self, *args, **options):
        self._create_data()