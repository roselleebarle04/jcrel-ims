from django.contrib import admin
<<<<<<< HEAD
from .models import Item, Supplier, Category, Brand, ItemModel, Account, AddArrival, Sale
=======
from .models import Item, Supplier, Accounts, AddArrival, Sale
>>>>>>> 8140a52e08722bace70efe4166e16b70e5b3c36a

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

