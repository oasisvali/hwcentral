from django.conf.urls import include, url
from django.contrib import admin

from core.routing.routers import static_csrf_cookie_router, dynamic_router, static_router
from core.utils.constants import HttpMethod
from hwcentral.urls.common import get_all_env_urlpatterns
from sphinx.urlnames import SphinxUrlNames
from sphinx.views import deal_post, tags_get


def get_debug_urlpatterns():
    return get_all_env_urlpatterns() + get_admin_urlpatterns() + get_sphinx_urlpatterns()


def get_admin_urlpatterns():
    return [
        url('^admin/doc/', include('django.contrib.admindocs.urls')),
        url('^admin/', include(admin.site.urls)),
    ]


def get_sphinx_urlpatterns():
    return [
        url(SphinxUrlNames.INDEX.url_matcher, static_csrf_cookie_router, {'template': SphinxUrlNames.INDEX.template},
            name=SphinxUrlNames.INDEX.name),
        url(SphinxUrlNames.DEAL.url_matcher, dynamic_router, {HttpMethod.POST: deal_post},
            name=SphinxUrlNames.DEAL.name),
        url(SphinxUrlNames.TAGS.url_matcher, dynamic_router, {HttpMethod.GET: tags_get},
            name=SphinxUrlNames.TAGS.name),
        url(SphinxUrlNames.REVISION.url_matcher, static_router, {'template': SphinxUrlNames.REVISION.template},
            name=SphinxUrlNames.REVISION.name)
    ]

urlpatterns = get_debug_urlpatterns()
