from django.contrib import admin
from .models import *



class AccountAdmin(admin.ModelAdmin):
	pass
admin.site.register(Account, AccountAdmin)

class ItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Item, ItemAdmin)

class SupplierAdmin(admin.ModelAdmin):
	pass
admin.site.register(Supplier, SupplierAdmin)

class CustomerAdmin(admin.ModelAdmin):
	pass
admin.site.register(Customer, CustomerAdmin)

class SaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sale, SaleAdmin)

class ItemSaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemSale, ItemSaleAdmin)

class TransferRecordAdmin(admin.ModelAdmin):
	pass
admin.site.register(TransferRecord, TransferRecordAdmin)

class ItemArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemArrival, ItemArrivalAdmin)

class ArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(Arrival, ArrivalAdmin)

class LocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Location, LocationAdmin)

class ItemLocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemLocation, ItemLocationAdmin)
