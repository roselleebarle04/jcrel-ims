from django.conf.urls import patterns, url

from inventory import views

urlpatterns = patterns('',
  url(r'^$', views.add_arrival, name='add_arrival'),
  url(r'^new$', views.arrival_create, name='arrival_new'),
  url(r'^edit/(?P<pk>\d+)$', views.arrival_update, name='arrival_edit'),
  url(r'^delete/(?P<pk>\d+)$', views.arrival_delete, name='arrival_delete'),
)