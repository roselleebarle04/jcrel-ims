from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin

from inventory import views as inventory_views

urlpatterns = [
    url(r'^$', inventory_views.dashboard, name='dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', inventory_views.signup, name="signup"),
    url(r'^login/$', auth_views.login, {'template_name':'accounts/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name':'accounts/logout.html'}),
    # url(r'^signup/$', inventory_views.signup, name='signup'),
    
    # Reporting Feature
    url(r'^reports/inventory/', inventory_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', inventory_views.sales_reports, name='sales_reports'),

    url(r'^items/$', inventory_views.items, name='items'),
    url(r'^add_item/$', inventory_views.add_item, name='add_item'),  

    url(r'^sales/$', inventory_views.sales, name='sales'),
    url(r'^add_sale/$', inventory_views.add_sale, name='add_sale'),

    url(r'^add_arrival/$', inventory_views.add_arrival, name='add_arrival'),
    url(r'^transfer_hist/$', inventory_views.transfer_hist, name = 'transfer_hist'),
    url(r'^transfer_form/$', inventory_views.create_transfer, name = 'transfer_form'),


]
