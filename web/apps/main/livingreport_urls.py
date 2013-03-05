from django.conf.urls.defaults import *

import livingreport

urlpatterns = patterns(
    '',

    # import livingreport urls in this way to preserve the url
    # namespace (like the admin)
    url(r'^', include(livingreport.namespace.urls)),
)


