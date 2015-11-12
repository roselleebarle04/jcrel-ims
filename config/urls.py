from django.conf.urls import include, url
from django.contrib import admin

from inventory import views as inventory_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', inventory_views.login, name='login'),
    url(r'^$', inventory_views.dashboard, name='dashboard'),
    
    # Reporting Feature
    url(r'^reports/inventory/', inventory_views.inventory_reports, name='inventory_reports'),
    url(r'^reports/sales/', inventory_views.sales_reports, name='sales_reports'),

    url(r'^add_arrival/$', inventory_views.add_arrival, name='add_arrival'),
]
