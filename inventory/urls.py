from django.conf.urls import include, url
from django.contrib import admin

from inventory import views as inventory_views

urlpatterns = [
    url(r'^$', inventory_views.dashboard, name='dashboard'),
	
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^login/$', inventory_views.login, name='login'),
    
    # Reporting Feature
    url(r'^reports/inventory/', inventory_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', inventory_views.sales_reports, name='sales_reports'),

    url(r'^$', inventory_views.arrival_list, name='arrival_list'),
  	url(r'^new$', inventory_views.arrival_create, name='arrival_new'),
  	url(r'^edit/(?P<pk>\d+)$', inventory_views.arrival_update, name='arrival_edit'),
  	url(r'^delete/(?P<pk>\d+)$', inventory_views.arrival_delete, name='arrival_delete'),
]