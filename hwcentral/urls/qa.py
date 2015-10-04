from django.conf.urls import url

from core.routing.routers import dynamic_router, static_csrf_cookie_router
from core.utils.constants import HttpMethod
from hwcentral.urls.debug import get_debug_urlpatterns
from sphinx.urlnames import SphinxUrlNames
from sphinx.views import deal_subpart_post

urlpatterns = get_debug_urlpatterns() + [
    url(SphinxUrlNames.INDEX.url_matcher, static_csrf_cookie_router, {'template': 'app.html'},
        name=SphinxUrlNames.INDEX.name),
    url(SphinxUrlNames.DEAL_SUBPART.url_matcher, dynamic_router, {HttpMethod.POST: deal_subpart_post},
        name=SphinxUrlNames.DEAL_SUBPART.url_matcher),
]
