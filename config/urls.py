from django.conf.urls import include, url
from django.contrib import admin

from inventory import views as inventory_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', inventory_views.dashboard, name='dashboard'),
    url(r'^reports/$', inventory_views.reports, name='reports'),
]
