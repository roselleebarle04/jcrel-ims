from django.contrib import admin
from .models import Item, Supplier, Category, Brand, ItemModel, Account, AddArrival, Sale

class AccountAdmin(admin.ModelAdmin):
	pass
admin.site.register(Account, AccountAdmin)

class ItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Item, ItemAdmin)

class SupplierAdmin(admin.ModelAdmin):
	pass
admin.site.register(Supplier, SupplierAdmin)

class CategoryAdmin(admin.ModelAdmin):
	pass
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
	pass
admin.site.register(Brand, BrandAdmin)

class ItemModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemModel, ItemModelAdmin)

class AddArrivalAdmin(admin.ModelAdmin):
	pass
admin.site.register(AddArrival)

class SaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sale, SaleAdmin)

