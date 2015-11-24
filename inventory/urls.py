from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import password_reset

from config import settings
from . import views as inventory_views
from . import reports as reports_views


urlpatterns = [
    url(r'^$', inventory_views.dashboard, name='dashboard'),

    url(r'^reports/inventory/', reports_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', reports_views.sales_reports, name='sales_reports'),

    url(r'^items/$', inventory_views.items, name='items'),
    url(r'^items/add/$', inventory_views.add_item, name='add_item'),
    url(r'^items/delete/(?P<item_id>[0-9]+)/$', inventory_views.delete_item, name = 'delete_item'), 
    url(r'^items/update/(?P<item_id>[0-9]+)/$', inventory_views.update_item, name = 'update_item'), 

    url(r'^suppliers/$', inventory_views.suppliers, name='suppliers'),
    url(r'^suppliers/add/$', inventory_views.add_supplier, name='add_supplier'),
    url(r'^suppliers/update/(?P<supplier_id>[0-9]+)/$', inventory_views.update_supplier, name='update_supplier'),
    url(r'^suppliers/delete/(?P<supplier_id>[0-9]+)/$', inventory_views.delete_supplier, name='delete_supplier'),

    url(r'^customers/$', inventory_views.customers, name='customers'),
    url(r'^customers/update/(?P<customers_id>[0-9]+)/$', inventory_views.update_customer, name='update_customer'),
    url(r'^customers/delete/(?P<customers_id>[0-9]+)/$', inventory_views.delete_customer, name='delete_customer'),

    url(r'^sale/$', inventory_views.sale, name='sale'),
    url(r'^sales/$', inventory_views.sales, name='sales'),
    url(r'^sales/add/$', inventory_views.add_sale, name = 'add_sale'),
    url(r'^sales/delete/(?P<sale_id>[0-9]+)/$', inventory_views.delete_sale, name = 'delete_sale'),
    url(r'^sale/update/(?P<sale_id>[0-9]+)/$', inventory_views.update_sale, name = 'update_sale'),

    url(r'^arrival/$', inventory_views.arrival, name='arrival'),
    url(r'^arrival/add/$', inventory_views.arrival, name='arrival'),
    url(r'^arrival/history/$', inventory_views.arrival_history, name='arrival_history'),

    url(r'^transfer_hist/$', inventory_views.transfer_hist, name = 'transfer_hist'),
    url(r'^transfer_form/$', inventory_views.create_transfer, name = 'new_transfer'),
    url(r'^transfer/delete/(?P<transfer_id>[0-9]+)/$$', inventory_views.transfer_delete, name='transfer_delete'),

    url(r'^location/$', inventory_views.location, name = 'location'),
    url(r'^location/delete/(?P<location_id>[0-9]+)/$$', inventory_views.location_delete, name='location_delete'),
]

    