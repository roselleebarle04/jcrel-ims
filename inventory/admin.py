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

class SoldItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(SoldItem, SoldItemAdmin)

class TransferItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer_item)

class Transferdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer)

class ArrivedItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(ArrivedItem, ArrivedItemAdmin)

class ArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(Arrival, ArrivalAdmin)

class RegisterArrivedItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(RegisterArrivedItem, RegisterArrivedItemAdmin)

class LocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Location)


class WarningItemsAdming(admin.ModelAdmin):
	pass
admin.site.register(WarningItems)

class ItemLocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemLocation)
