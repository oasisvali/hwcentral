from django.conf.urls import url

from core.routing.routers import dynamic_router
from core.utils.constants import HttpMethod
from core.views import test_500_get
from hwcentral.urls.common import get_all_env_urlpatterns

urlpatterns = get_all_env_urlpatterns() + get_admin_urlpatterns() + [
    # add a error page view to test error page
    url('^tTrNJnEzCxJfqtDBtWO2cOo6dsA/', dynamic_router, {HttpMethod.GET: test_500_get})
]