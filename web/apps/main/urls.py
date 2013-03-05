from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from main.views import employee_list, employee_profile

# Main urls.
urlpatterns = patterns('',    
    url(r'^$', employee_list, name="employee-list"),
    url(r'^(\d+)/$', employee_profile, name="employee-profile"),
)

# Admin views.
# admin.autodiscover()
urlpatterns += patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# Login and logout.
urlpatterns += patterns(
    '',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', 
        name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',
        name="logout"),
    url(r'^accounts/change-password/$', 
        'django.contrib.auth.views.password_change', 
        name="password_change"),
    url(r'^accounts/change-password-done/$', 
        'django.contrib.auth.views.password_change_done', 
        name="password_change_done"),
)

# Error views.
handler500 = 'django.views.defaults.server_error'
handler404 = 'django.views.defaults.page_not_found'

# Hack for serving media when using Django's development server. Doesn't work
# when running apache on server.
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
