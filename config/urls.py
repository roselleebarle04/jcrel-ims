
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import password_reset

from . import settings
from inventory import views as inventory_views
from inventory import urls as inventory_urls


urlpatterns = [
    url(r'^', include(inventory_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', inventory_views.signup, name="signup"),
    url(r'^login/$', auth_views.login, {'template_name':'accounts/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name':'accounts/logout.html'}),
    url(r'^change_password/$', inventory_views.change_password, name="change_password"),
    url(r'^notifications/$', inventory_views.notifications, name="notifications"),

    url(r'^password_reset/$', auth_views.password_reset, 
        {'template_name':'accounts/password_reset_form.html', 'email_template_name':'accounts/password_reset_email.html',
        'subject_template_name':'accounts/password_reset_subject.txt'}, name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name':'accounts/password_reset_done.html'},
        name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name':'accounts/password_reset_confirm.html'}, 
        name="password_reset_confirm"),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name':'accounts/password_reset_complete.html'},
        name="password_reset_complete"),
    url(r'^password_change/$', auth_views.password_change, {'template_name':'accounts/password_change_form.html'},
        name="password_change"),
    url(r'^password_change/done/$', auth_views.password_change_done, {'template_name':'registration/password_change_done.html'},
        name="password_change_done"),

    # # url(r'^/accounts/password/reset/$', password_reset, {'template_name': 'my_templates/password_reset.html'}),

    # # url(r'^signup/$', inventory_views.signup, name='signup'),
    
    # # Reporting Feature
    # # url(r'^reports/inventory/', inventory_views.inventory_reports, name='inventory_reports'),
    # # url(r'^reports/sales/', inventory_views.sales_reports, name='sales_reports'),

    # url(r'^items/$', inventory_views.items, name='items'),
    # url(r'^items/add/$', inventory_views.add_item, name='add_item'),
    # url(r'^items/delete/(?P<item_id>[0-9]+)/$', inventory_views.delete_item, name = 'delete_item'), 
    # url(r'^items/update/(?P<item_id>[0-9]+)/$', inventory_views.update_item, name = 'update_item'), 

    # # Suppliers 
    # url(r'^suppliers/$', inventory_views.suppliers, name='suppliers'),
    # url(r'^suppliers/add/$', inventory_views.add_supplier, name='add_supplier'),
    # url(r'^suppliers/update/(?P<supplier_id>[0-9]+)/$', inventory_views.update_supplier, name='update_supplier'),
    # url(r'^suppliers/delete/(?P<supplier_id>[0-9]+)/$', inventory_views.delete_supplier, name='delete_supplier'),

    # # Account Settings
    # url(r'^settings/$', inventory_views.settings, name='settings'),
    # # url(r'^suppliers/add/$', inventory_views.add_supplier, name='add_supplier'),
    # url(r'^settings/update_settings_photo/(?P<user_id>[0-9]+)/$', inventory_views.update_settings_photo,
    #  name='update_settings_photo'),
    # # url(r'^suppliers/delete/(?P<supplier_id>[0-9]+)/$', inventory_views.delete_supplier, name='delete_supplier'),


    # url(r'^customers/$', inventory_views.customers, name='customers'),
    # url(r'^customers/update/(?P<customers_id>[0-9]+)/$', inventory_views.update_customer, name='update_customer'),
    # url(r'^customers/delete/(?P<customers_id>[0-9]+)/$', inventory_views.delete_customer, name='delete_customer'),

    # url(r'^sales/$', inventory_views.sales, name='sales'),
    # url(r'^sales/history/$', inventory_views.sales_history, name='history'),
    # url(r'^sales/add/$', inventory_views.add_sale, name = 'add_sale'),
    # url(r'^sales/delete/(?P<sale_id>[0-9]+)/$', inventory_views.delete_sale, name = 'delete_sale'),
    # url(r'^sale/$', inventory_views.sales, name='sale'),


    # #=================================================================
    # url(r'^sale/$', inventory_views.sales, name='sale'),
    # url(r'^sale/update/(?P<sale_id>[0-9]+)/$', inventory_views.update_sale, name = 'update_sale'),

    # url(r'^sale/update/(?P<sale_id>[0-9]+)/$', inventory_views.update_sale, name = 'update_sale'),

    
    # # url(r'^arrivals/$', inventory_views.arrivals, name = 'arrivals'),
    # # url(r'^arrivals/add/$', inventory_views.arrival_create, name = 'arrival_form'),    
    # # url(r'^arrivals/delete/(?P<arrival_id>[0-9]+)/$', inventory_views.arrival_delete, name='arrival_delete'),
    # # url(r'^arrivals/update/(?P<arrival_id>[0-9]+)/$', inventory_views.arrival_update, name='arrival_update'),


    # url(r'^settings/$', inventory_views.settings, name='settings'),

    # # url(r'^arrivals/$', inventory_views.arrivals, name = 'arrivals'),
    # # url(r'^arrivals/add/$', inventory_views.arrival_create, name = 'arrival_form'),    
    # url(r'^arrivals/delete/(?P<arrival_id>[0-9]+)/$', inventory_views.arrival_delete, name='arrival_delete'),
    # # url(r'^arrivals/update/(?P<arrival_id>[0-9]+)/$', inventory_views.arrival_delete, name='arrival_delete'),

    # url(r'^arrival/$', inventory_views.arrival, name='arrival'),
    # url(r'^arrival/add/$', inventory_views.arrival, name='arrival'),
    # url(r'^arrival/history/$', inventory_views.arrival_history, name='arrival_history'),

    # url(r'^transfer_hist/$', inventory_views.transfer_hist, name = 'transfer_hist'),
    # url(r'^transfer_form/$', inventory_views.create_transfer, name = 'new_transfer'),
    # url(r'^transfer/delete/(?P<transfer_id>[0-9]+)/$$', inventory_views.transfer_delete, name='transfer_delete'),

    # url(r'^location/$', inventory_views.location, name = 'location'),
    # url(r'^location/delete/(?P<location_id>[0-9]+)/$$', inventory_views.location_delete, name='location_delete'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
