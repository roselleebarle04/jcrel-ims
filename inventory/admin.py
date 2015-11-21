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

class AddArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(AddArrival)

class SaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sale, SaleAdmin)

class TransferItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer_item)

class LocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Location)


