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
    assignment_post, assignment_override_get, assignment_override_post, secure_static_get, announcements_ajax_get, \
    question_set_choice_widget_override_ajax_get, question_set_choice_widget_ajax_get, completion_chart_get, \
    parent_focus_id_get, focus_id_get, single_focus_student_chart_get, focusroom_chart_get, practice_get, practice_post
from core.views import logout_wrapper
from edge.urlnames import EdgeUrlNames
from edge.views import index_get as edge_index_get, subject_id_get as edge_subject_id_get, \
    student_id_get as edge_student_id_get
from ink.urlnames import InkUrlNames
from ink.views import index_get as ink_index_get, index_post as ink_index_post, parent_id_get, parent_id_post
from lodge.urlnames import LodgeUrlNames
from lodge.views import index_get as lodge_index_get


def get_ink_urlpatterns():
    return [
        url(InkUrlNames.INDEX.url_matcher, dynamic_router,
            {HttpMethod.GET: ink_index_get, HttpMethod.POST: ink_index_post},
            name=InkUrlNames.INDEX.name),
        url(InkUrlNames.PARENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: parent_id_get, HttpMethod.POST: parent_id_post}, name=InkUrlNames.PARENT_ID.name)
    ]


def get_edge_urlpatterns():
    return [
        url(EdgeUrlNames.INDEX.url_matcher, dynamic_router, {HttpMethod.GET: edge_index_get},
            name=EdgeUrlNames.INDEX.name),
        url(EdgeUrlNames.SUBJECT_ID.url_matcher, dynamic_router, {HttpMethod.GET: edge_subject_id_get},
            name=EdgeUrlNames.SUBJECT_ID.name),
        url(EdgeUrlNames.STUDENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: edge_student_id_get},
            name=EdgeUrlNames.STUDENT_ID.name)

    ]

def get_all_mode_urlpatterns():
    return [
        UrlNames.INDEX.create_index_route(),

        # UrlNames.ABOUT.create_static_route(),

        # secure-static must still be available while sleeping otherwise grading (specifically, shell submission creation) fails
        # TODO: this is a hack, fix it, no reason for secure static to be exposed while sleeping
        url(UrlNames.SECURE_STATIC.url_matcher, dynamic_router, {HttpMethod.GET: secure_static_get},
            name=UrlNames.SECURE_STATIC.name),

        url(LodgeUrlNames.INDEX.url_matcher, dynamic_router, {HttpMethod.GET: lodge_index_get},
            name=LodgeUrlNames.INDEX.name)
    ]


def get_all_env_urlpatterns():
    common_urlpatterns = get_all_mode_urlpatterns() + get_ink_urlpatterns() + get_edge_urlpatterns()

    common_urlpatterns += [
        # using django's inbuilt auth views for auth-specific tasks
        url(UrlNames.LOGIN.url_matcher, login_wrapper(login),
            {'template_name': UrlNames.LOGIN.get_template()}, name=UrlNames.LOGIN.name),

        url(UrlNames.LOGOUT.url_matcher, logout_wrapper(logout),
            {'next_page': UrlNames.INDEX.name},
            name=UrlNames.LOGOUT.name),

        url(r'^forgot-password/$', password_reset, {
            'template_name': 'forgot_password/form.html',
            'html_email_template_name': 'forgot_password/html_body.html',
            'email_template_name': 'forgot_password/text_body.html',
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
        url(UrlNames.HOME.url_matcher, dynamic_router, {HttpMethod.GET: home_get},
            name=UrlNames.HOME.name),

        url(UrlNames.SETTINGS.url_matcher, dynamic_router, {HttpMethod.GET: settings_get},
            name=UrlNames.SETTINGS.name),

        url(UrlNames.SUBJECT_ID.url_matcher, dynamic_router, {HttpMethod.GET: subject_id_get},
            name=UrlNames.SUBJECT_ID.name),
        url(UrlNames.PARENT_SUBJECT_ID.url_matcher, dynamic_router,
            {HttpMethod.GET: parent_subject_id_get},
            name=UrlNames.PARENT_SUBJECT_ID.name),

        url(UrlNames.FOCUS_ID.url_matcher, dynamic_router, {HttpMethod.GET: focus_id_get},
            name=UrlNames.FOCUS_ID.name),
        url(UrlNames.PARENT_FOCUS_ID.url_matcher, dynamic_router,
            {HttpMethod.GET: parent_focus_id_get},
            name=UrlNames.PARENT_FOCUS_ID.name),

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
        url(UrlNames.SINGLE_FOCUS_STUDENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: single_focus_student_chart_get},
            name=UrlNames.SINGLE_FOCUS_STUDENT_CHART.name),
        url(UrlNames.SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: subjectroom_chart_get},
            name=UrlNames.SUBJECTROOM_CHART.name),
        url(UrlNames.FOCUSROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: focusroom_chart_get},
            name=UrlNames.FOCUSROOM_CHART.name),
        url(UrlNames.SUBJECT_TEACHER_SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: subject_teacher_subjectroom_chart_get},
            name=UrlNames.SUBJECT_TEACHER_SUBJECTROOM_CHART.name),
        url(UrlNames.CLASS_TEACHER_SUBJECTROOM_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: class_teacher_subjectroom_chart_get},
            name=UrlNames.CLASS_TEACHER_SUBJECTROOM_CHART.name),
        url(UrlNames.ASSIGNMENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: assignment_chart_get},
            name=UrlNames.ASSIGNMENT_CHART.name),
        url(UrlNames.COMPLETION_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: completion_chart_get},
            name=UrlNames.COMPLETION_CHART.name),
        url(UrlNames.STANDARD_ASSIGNMENT_CHART.url_matcher, dynamic_router,
            {HttpMethod.GET: standard_assignment_chart_get},
            name=UrlNames.STANDARD_ASSIGNMENT_CHART.name),


        url(UrlNames.ANNOUNCEMENTS_AJAX.url_matcher, dynamic_router, {HttpMethod.GET: announcements_ajax_get}, name=UrlNames.ANNOUNCEMENTS_AJAX.name),
        url(UrlNames.QUESTION_SET_CHOICE_WIDGET_AJAX.url_matcher, dynamic_router, {HttpMethod.GET: question_set_choice_widget_ajax_get}, name=UrlNames.QUESTION_SET_CHOICE_WIDGET_AJAX.name),
        url(UrlNames.QUESTION_SET_CHOICE_WIDGET_OVERRIDE_AJAX.url_matcher, dynamic_router, {HttpMethod.GET: question_set_choice_widget_override_ajax_get}, name=UrlNames.QUESTION_SET_CHOICE_WIDGET_OVERRIDE_AJAX.name),



        url(UrlNames.ANNOUNCEMENT.url_matcher, dynamic_router, {HttpMethod.GET: announcement_get,
                                                                HttpMethod.POST: announcement_post},
            name=UrlNames.ANNOUNCEMENT.name),
        url(UrlNames.PRACTICE.url_matcher, dynamic_router, {HttpMethod.GET: practice_get,
                                                            HttpMethod.POST: practice_post},
            name=UrlNames.PRACTICE.name),

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
