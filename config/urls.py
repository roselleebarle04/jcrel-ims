
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import password_reset

from apps.inventory import views as inventory_views
from apps.inventory import urls as inventory_urls
from apps.inventory import accounts as account_views


urlpatterns = [
    url(r'^', include(inventory_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$', account_views.signup, name="signup"),
    url(r'^login/$', auth_views.login, {'template_name':'accounts/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name':'accounts/login.html'}),
    url(r'^change_password/$', account_views.change_password, name="change_password"),
    url(r'^notifications/$', account_views.notifications, name="notifications"),
    # url('^inbox   /notifications/', include(notifications.urls)),

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

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
