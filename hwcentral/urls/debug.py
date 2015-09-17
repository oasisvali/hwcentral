from django.conf.urls import include, url
from django.contrib.auth.views import logout, login, password_reset_confirm, password_reset_done, password_reset, \
    password_reset_complete
from django.contrib import admin

from core.forms.password import CustomSetPasswordForm
from core.routing.routers import dynamic_router, static_router
from core.routing.urlnames import UrlNames
from core.utils.constants import HttpMethod
from core.views import home_get, settings_get, announcement_get, announcement_post, assignment_get, \
    student_chart_get, \
    subjectroom_chart_get,single_subject_student_chart_get, subject_teacher_subjectroom_chart_get, \
    class_teacher_subjectroom_chart_get, assignment_chart_get, password_get, password_post, \
    standard_assignment_chart_get, assignment_post, \
    secure_static_get, subject_id_get, classroom_id_get, assignment_id_get, submission_id_get, \
    submission_id_post, assignment_preview_id_get, index_get, assignment_override_get, assignment_override_post, \
    login_wrapper, logout_wrapper, parent_subject_id_get, test_500_get
from hwcentral import settings
from hwcentral.urls.common import get_common_urlpatterns

urlpatterns = get_common_urlpatterns() + [
    url('^admin/doc/', include('django.contrib.admindocs.urls')),
    url('^admin/', include(admin.site.urls)),
]

