from django.conf.urls import url

from core.routing.routers import static_router
from core.routing.urlnames import UrlNames
from hwcentral.urls.common import get_all_mode_urlpatterns

SLEEP_MODE_CONTEXT = {'sleep_mode': True}

urlpatterns = get_all_mode_urlpatterns() + [
    UrlNames.ABOUT.create_static_route(SLEEP_MODE_CONTEXT),

    # login url entry is required as the login urlname needs to be set for the index page to work
    url(UrlNames.LOGIN.url_matcher, static_router,
        {'template': '503.html', 'context': SLEEP_MODE_CONTEXT, 'status': 503}, name=UrlNames.LOGIN.name),
    url(r'^.+?/$', static_router , {'template': '503.html', 'context': SLEEP_MODE_CONTEXT, 'status': 503}),
]
