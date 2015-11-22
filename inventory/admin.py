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

class ArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(Arrival, ArrivalAdmin)

class ArrivedItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(ArrivedItem, ArrivedItemAdmin)

class SaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sale, SaleAdmin)

class TransferItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer_item)

class LocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Location)
class ItemPurchaseAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemPurchase, ItemPurchaseAdmin)

class PurchaseAdmin(admin.ModelAdmin):
	pass
admin.site.register(Purchase, PurchaseAdmin)
