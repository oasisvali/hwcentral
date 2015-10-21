from django.conf.urls import url
from django.contrib.auth.views import password_reset_complete, password_reset_confirm, password_reset_done, \
    password_reset, login, logout

from core.forms.password import CustomSetPasswordForm
from core.routing.routers import dynamic_router
from core.routing.urlnames import UrlNames
from core.utils.constants import HttpMethod
from core.views import login_wrapper, home_get, settings_get, subject_id_get, classroom_id_get, \
    parent_subject_id_get, assignment_id_get, assignment_preview_id_get, student_chart_get, \
    single_subject_student_chart_get, subjectroom_chart_get, subject_teacher_subjectroom_chart_get, \
    class_teacher_subjectroom_chart_get, assignment_chart_get, standard_assignment_chart_get, announcement_get, \
    announcement_post, password_get, password_post, submission_id_get, submission_id_post, assignment_get, \
    assignment_post, assignment_override_get, assignment_override_post, secure_static_get
from core.views import logout_wrapper


def get_all_mode_urlpatterns():
    return [
        UrlNames.INDEX.create_index_route(),
        # secure-static must still be available while sleeping otherwise grading (specifically, shell submission creation) fails
        url(UrlNames.SECURE_STATIC.url_matcher, dynamic_router, {HttpMethod.GET: secure_static_get},
            name=UrlNames.SECURE_STATIC.name),
    ]


def get_all_env_urlpatterns():
    common_urlpatterns = get_all_mode_urlpatterns()

    common_urlpatterns += [
        # using django's inbuilt auth views for auth-specific tasks
        url(UrlNames.LOGIN.url_matcher, login_wrapper(login),
            {'template_name': UrlNames.LOGIN.get_template()}, name=UrlNames.LOGIN.name),

        url(UrlNames.LOGOUT.url_matcher, logout_wrapper(logout),
            {'next_page': UrlNames.INDEX.name},
            name=UrlNames.LOGOUT.name),

        url(r'^forgot-password/$', password_reset, {
            'template_name': 'forgot_password/form.html',
            'email_template_name': 'forgot_password/email_body.html',
            'subject_template_name': 'forgot_password/email_subject.html'
        },
            name="forgot_password"),

        url(r'^forgot-password/mailed/$', password_reset_done, {
            'template_name': 'forgot_password/mailed.html'
        },
            name="password_reset_done"),

        #
        # used by both activation script and forgot passsword
        #
        url(r'^password-reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {
            'template_name': 'password_reset/form.html',
            'set_password_form': CustomSetPasswordForm
        },
            name="password_reset"),

        url(r'^password-reset/complete/$', password_reset_complete,
            {'template_name': 'password_reset/complete.html'},
            name="password_reset_complete"),
    ]

    # Adding the core-app urls
    common_urlpatterns += [
        UrlNames.ABOUT.create_static_route(),

        # url(UrlNames.REGISTER.url_matcher, dynamic_router,
        # {HttpMethod.GET: register_get, HttpMethod.POST: register_post},
        #     name=UrlNames.REGISTER.name),

        url(UrlNames.HOME.url_matcher, dynamic_router, {HttpMethod.GET: home_get},
            name=UrlNames.HOME.name),

        url(UrlNames.SETTINGS.url_matcher, dynamic_router, {HttpMethod.GET: settings_get},
            name=UrlNames.SETTINGS.name),

        url(UrlNames.SUBJECT_ID.url_matcher, dynamic_router, {HttpMethod.GET: subject_id_get},
            name=UrlNames.SUBJECT_ID.name),
        url(UrlNames.PARENT_SUBJECT_ID.url_matcher, dynamic_router,
            {HttpMethod.GET: parent_subject_id_get},
            name=UrlNames.PARENT_SUBJECT_ID.name),

        url(UrlNames.CLASSROOM_ID.url_matcher, dynamic_router, {HttpMethod.GET: classroom_id_get},
            name=UrlNames.CLASSROOM_ID.name),

        url(UrlNames.ASSIGNMENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: assignment_id_get},
            name=UrlNames.ASSIGNMENT_ID.name),
        url(UrlNames.ASSIGNMENT_PREVIEW_ID.url_matcher, dynamic_router,
            {HttpMethod.GET: assignment_preview_id_get},
            name=UrlNames.ASSIGNMENT_PREVIEW_ID.name),

        url(UrlNames.SUBMISSION_ID.url_matcher, dynamic_router, {HttpMethod.GET: submission_id_get,
                                                                 HttpMethod.POST: submission_id_post},
            name=UrlNames.SUBMISSION_ID.name),

        url(UrlNames.STUDENT_CHART.url_matcher, dynamic_router, {HttpMethod.GET: student_chart_get},
            name=UrlNames.STUDENT_CHART.name),
        url(UrlNames.SINGLE_SUBJECT_STUDENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: single_subject_student_chart_get},
            name=UrlNames.SINGLE_SUBJECT_STUDENT_CHART.name),
        url(UrlNames.SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: subjectroom_chart_get},
            name=UrlNames.SUBJECTROOM_CHART.name),
        url(UrlNames.SUBJECT_TEACHER_SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: subject_teacher_subjectroom_chart_get},
            name=UrlNames.SUBJECT_TEACHER_SUBJECTROOM_CHART.name),
        url(UrlNames.CLASS_TEACHER_SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: class_teacher_subjectroom_chart_get},
            name=UrlNames.CLASS_TEACHER_SUBJECTROOM_CHART.name),
        url(UrlNames.ASSIGNMENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: assignment_chart_get},
            name=UrlNames.ASSIGNMENT_CHART.name),
        url(UrlNames.STANDARD_ASSIGNMENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: standard_assignment_chart_get},
            name=UrlNames.STANDARD_ASSIGNMENT_CHART.name),

        url(UrlNames.ANNOUNCEMENT.url_matcher, dynamic_router, {HttpMethod.GET: announcement_get,
                                                                HttpMethod.POST: announcement_post},
            name=UrlNames.ANNOUNCEMENT.name),

        url(UrlNames.PASSWORD.url_matcher, dynamic_router, {HttpMethod.GET: password_get,
                                                            HttpMethod.POST: password_post},
            name=UrlNames.PASSWORD.name),

        url(UrlNames.ASSIGNMENT.url_matcher, dynamic_router, {HttpMethod.GET: assignment_get,
                                                              HttpMethod.POST: assignment_post},
            name=UrlNames.ASSIGNMENT.name),
        url(UrlNames.ASSIGNMENT_OVERRIDE.url_matcher, dynamic_router,
            {HttpMethod.GET: assignment_override_get,
             HttpMethod.POST: assignment_override_post},
            name=UrlNames.ASSIGNMENT_OVERRIDE.name),
    ]

    return common_urlpatterns
