from django.conf.urls import url

from core.routing.routers import dynamic_router
from core.utils.constants import HttpMethod
from croupier.urlnames import CroupierUrlNames
from croupier.views import deal_subpart_post
from hwcentral.urls.debug import get_debug_urlpatterns

urlpatterns = get_debug_urlpatterns() + [
    url(CroupierUrlNames.DEAL_SUBPART.url_matcher, dynamic_router, {HttpMethod.POST: deal_subpart_post},
        name=CroupierUrlNames.DEAL_SUBPART.url_matcher),
]
