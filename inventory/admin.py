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

# class ArrivalAdmin(admin.ModelAdmin):
# 	pass
# admin.site.register(Arrival, ArrivalAdmin)

# class ArrivedItemAdmin(admin.ModelAdmin):
# 	pass
# admin.site.register(ArrivedItem, ArrivedItemAdmin)

class SaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sale, SaleAdmin)

class TransferItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer_item, TransferItemAdmin)

class TransferAdmin(admin.ModelAdmin):
	pass
admin.site.register(Transfer, TransferAdmin)

class ArrivedItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(ArrivedItem, ArrivedItemAdmin)

class ArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(Arrival, ArrivalAdmin)

class LocationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Location)


