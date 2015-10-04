from django.conf.urls import include, url
from django.contrib import admin

from core.routing.routers import static_csrf_cookie_router, dynamic_router
from core.utils.constants import HttpMethod
from hwcentral.urls.common import get_all_env_urlpatterns
from sphinx.urlnames import SphinxUrlNames
from sphinx.views import deal_subpart_post, download_json_get


def get_debug_urlpatterns():
    return get_all_env_urlpatterns() + [
        url('^admin/doc/', include('django.contrib.admindocs.urls')),
        url('^admin/', include(admin.site.urls)),
    ] + [
               url(SphinxUrlNames.INDEX.url_matcher, static_csrf_cookie_router, {'template': 'app.html'},
                   name=SphinxUrlNames.INDEX.name),
               url(SphinxUrlNames.DEAL_SUBPART.url_matcher, dynamic_router, {HttpMethod.POST: deal_subpart_post},
                   name=SphinxUrlNames.DEAL_SUBPART.name),
        url(SphinxUrlNames.DOWNLOAD_JSON.url_matcher, dynamic_router, {HttpMethod.GET: download_json_get},
            name=SphinxUrlNames.DOWNLOAD_JSON.name),
    ]


urlpatterns = get_debug_urlpatterns()
