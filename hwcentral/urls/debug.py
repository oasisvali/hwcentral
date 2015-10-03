from django.conf.urls import include, url
from django.contrib import admin

from hwcentral.urls.common import get_all_env_urlpatterns


def get_debug_urlpatterns():
    return get_all_env_urlpatterns() + [
        url('^admin/doc/', include('django.contrib.admindocs.urls')),
        url('^admin/', include(admin.site.urls)),
    ]


urlpatterns = get_debug_urlpatterns()
