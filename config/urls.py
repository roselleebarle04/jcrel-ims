from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import password_reset


from . import settings
from inventory import views as inventory_views

urlpatterns = [
    url(r'^$', inventory_views.dashboard, name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', inventory_views.signup, name="signup"),
    url(r'^login/$', auth_views.login, {'template_name':'accounts/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name':'accounts/logout.html'}),
    url(r'^change_password/$', inventory_views.change_password, name="change_password"),
    url(r'^notifications/$', inventory_views.notifications, name="notifications"),
    # url(r'^forgot_password/$', inventory_views.forgot_password, name="forgot_password"),

    #password reset
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

    # url(r'^/accounts/password/reset/$', password_reset, {'template_name': 'my_templates/password_reset.html'}),

    # url(r'^signup/$', inventory_views.signup, name='signup'),
    
    # Reporting Feature
    url(r'^reports/inventory/', inventory_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', inventory_views.sales_reports, name='sales_reports'),

    url(r'^items/$', inventory_views.items, name='items'),
    url(r'^items/delete/(?P<item_id>[0-9]+)/$', inventory_views.delete_item, name = 'delete_item'), 
    url(r'^items/update/(?P<item_id>[0-9]+)/$', inventory_views.update_item, name = 'update_item'), 

    # Suppliers 
    url(r'^suppliers/$', inventory_views.suppliers, name='suppliers'),
    url(r'^suppliers/update/(?P<supplier_id>[0-9]+)/$', inventory_views.update_supplier, name='update_supplier'),
    url(r'^suppliers/delete/(?P<supplier_id>[0-9]+)/$', inventory_views.delete_supplier, name='delete_supplier'),

    url(r'^customers/$', inventory_views.customers, name='customers'),
    url(r'^customers/update/(?P<customers_id>[0-9]+)/$', inventory_views.update_customer, name='update_customer'),
    url(r'^customers/delete/(?P<customers_id>[0-9]+)/$', inventory_views.delete_customer, name='delete_customer'),

    url(r'^sales/$', inventory_views.sales, name='sales'),
    url(r'^sales/delete/(?P<sale_id>[0-9]+)/$', inventory_views.delete_sale, name = 'delete_sale'),
    url(r'^sales/update/(?P<sale_id>[0-9]+)/$', inventory_views.update_sale, name = 'update_sale'),

    url(r'^arrival/$', inventory_views.arrival, name='arrival'),
    url(r'^purchase/$', inventory_views.purchase, name='purchase'),

    url(r'^transfer_hist/$', inventory_views.transfer_hist, name = 'transfer_hist'),
    url(r'^transfer/delete/(?P<transfer_id>[0-9]+)/$$', inventory_views.transfer_delete, name='transfer_delete'),
    url(r'^location/$', inventory_views.location, name = 'location'),
    url(r'^location/delete/(?P<location_id>[0-9]+)/$$', inventory_views.location_delete, name='location_delete'),


    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # url(r'^reset/$', 'inventory.views.reset', name='reset'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            # 'inventory.views.reset_confirm', name='password_reset_confirm'),
    # url(r'^success/$', 'inventory.views.success', name='success'),
]

