from django.contrib import admin
from .models import Item, Supplier, Accounts, AddArrival, Sale

class AccountsAdmin(admin.ModelAdmin):
	pass
admin.site.register(Accounts, AccountsAdmin)

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

