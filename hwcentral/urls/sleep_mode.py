from django.conf.urls import url
from core.routing.routers import static_router
from core.routing.urlnames import UrlNames

SLEEP_MODE_CONTEXT = {'sleep_mode': True}

urlpatterns = [
    UrlNames.ABOUT.create_static_route(SLEEP_MODE_CONTEXT),
    UrlNames.INDEX.create_static_route(SLEEP_MODE_CONTEXT),
    url(UrlNames.LOGIN.url_matcher, static_router,
        {'template': '503.html', 'context': SLEEP_MODE_CONTEXT, 'status': 503}, name=UrlNames.LOGIN.name),
    url(r'^.+?/$', static_router , {'template': '503.html', 'context': SLEEP_MODE_CONTEXT, 'status': 503}),
]
