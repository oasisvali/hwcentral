from django.conf.urls import url

from core.routing.routers import static_router
from core.routing.urlnames import UrlNames
from hwcentral.urls.common import get_all_mode_urlpatterns

urlpatterns = get_all_mode_urlpatterns() + [
    # login url entry is required as the login urlname needs to be set for the index page to work
    url(UrlNames.LOGIN.url_matcher, static_router,
        {'template': '503.html', 'status': 503}, name=UrlNames.LOGIN.name),
    url(r'^.+?/$', static_router, {'template': '503.html', 'status': 503}),
]
