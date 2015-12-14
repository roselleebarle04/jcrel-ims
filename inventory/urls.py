
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import password_reset

from config import settings
from . import views as inventory_views
from . import reports as reports_views
from . import accounts as account_views
from . import history as history_views

urlpatterns = [
    url(r'^$', inventory_views.landing_page, name='landing_page'),
    url(r'^dashboard/$', inventory_views.dashboard, name='dashboard'),

    url(r'^reports/data/', reports_views.reports_data, name='reports_data'),
    url(r'^reports/charts/', reports_views.charts, name='charts'),
    url(r'^reports/inventory/', reports_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', reports_views.sales_reports, name='sales_reports'),

    url(r'^items/$', inventory_views.list_items, name='list_items'),
    url(r'^items/add/$', inventory_views.add_item, name='add_item'),
    url(r'^items/delete/(?P<item_id>[0-9]+)/$', inventory_views.delete_item, name = 'delete_item'), 
    url(r'^items/update/(?P<item_id>[0-9]+)/$', inventory_views.update_item, name = 'update_item'), 

    url(r'^suppliers/$', inventory_views.suppliers, name='suppliers'),
    url(r'^suppliers/add/$', inventory_views.add_supplier, name='add_supplier'),
    url(r'^suppliers/update/(?P<supplier_id>[0-9]+)/$', inventory_views.update_supplier, name='update_supplier'),
    url(r'^suppliers/delete/(?P<supplier_id>[0-9]+)/$', inventory_views.delete_supplier, name='delete_supplier'),

    url(r'^customers/$', inventory_views.customers, name='customers'),
    url(r'^customers/add/$', inventory_views.add_customer, name='add_customer'),
    url(r'^customers/update/(?P<customer_id>[0-9]+)/$', inventory_views.update_customer, name='update_customer'),
    url(r'^customers/delete/(?P<customer_id>[0-9]+)/$', inventory_views.delete_customer, name='delete_customer'),

    url(r'^sales/$', inventory_views.sales, name='sales'),
    url(r'^sales/history/$', history_views.sales_history, name='sales_history'),
   
    url(r'^arrival/$', inventory_views.arrival, name='arrival'),
    url(r'^arrival/add/$', inventory_views.arrival, name='arrival'),
    url(r'^arrival/delete/(?P<arrival_id>[0-9]+)/$$', inventory_views.arrival_delete, name='arrival_delete'),
    url(r'^arrival/history/$', history_views.arrival_history, name='arrival_history'),

    url(r'^transfer/history/$', history_views.transfer_history, name='transfer_history'),
    url(r'^transfer/add/$', inventory_views.create_transfer, name = 'create_transfer'),

    url(r'^location/$', inventory_views.list_locations, name='location'),
    url(r'^location/add/$', inventory_views.add_location, name = 'add_location'),
    url(r'^location/delete/(?P<location_id>[0-9]+)/$$', inventory_views.delete_location, name='delete_location'),
    url(r'^location/update/(?P<location_id>[0-9]+)/$', inventory_views.update_location, name='update_location'),

    url(r'^settings/$', account_views.settings, name='settings'),
    url(r'^settings/update_settings/$', account_views.update_settings,
     name='update_settings'),
]

    