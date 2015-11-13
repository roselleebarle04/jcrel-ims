from django.conf.urls import include, url
from django.contrib import admin

from inventory import views as inventory_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', inventory_views.login, name='login'),
    url(r'^$', inventory_views.dashboard, name='dashboard'),
    url(r'^reports/$', inventory_views.reports, name='reports'),
    url(r'^add_arrival/$', inventory_views.add_arrival, name='add_arrival'),
    url(r'^transfer_form/$', inventory_views.transfer_form, name = 'transfer_form'),

]
