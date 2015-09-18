from django.conf.urls import url

from core.routing.routers import dynamic_router
from core.utils.constants import HttpMethod
from core.views import test_500_get
from hwcentral.urls.common import get_common_urlpatterns

urlpatterns = get_common_urlpatterns() + [
    # add a error page view to test error page
    url('^tTrNJnEzCxJfqtDBtWO2cOo6dsA/', dynamic_router, {HttpMethod.GET: test_500_get})
]