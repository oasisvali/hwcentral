import django
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login, password_reset_confirm, password_reset_done, password_reset, \
    password_reset_complete
from django.contrib import admin
from django.contrib.sites.models import Site

import core
from core.forms.password import ResetPasswordForm
from core.utils.auth_check_wrappers import requires_auth_strict, requires_noauth_strict
from core.routing.routers import dynamic_router
from core.routing.urlnames import UrlNames
from core.utils.constants import HttpMethod
from core.views import home_get, settings_get, announcement_get, announcement_post, assignment_get, \
    student_chart_get, \
    subjectroom_chart_get,single_subject_student_chart_get, subject_teacher_subjectroom_chart_get, \
    class_teacher_subjectroom_chart_get, assignment_chart_get, password_get, password_post, \
    standard_assignment_chart_get, assignment_post, \
    secure_static_get, subject_id_get, classroom_id_get, assignment_id_get, submission_id_get, \
    submission_id_post, assignment_preview_id_get, index_get
from hwcentral import settings


if settings.DEBUG:
    CUSTOM_DOMAIN = 'localhost:8000'
else:
    CUSTOM_DOMAIN = None
# using django's inbuilt auth views for auth-specific tasks
urlpatterns = patterns(django.contrib.auth.views,

                       url(UrlNames.LOGIN.url_matcher, requires_noauth_strict(login),
                           {'template_name': UrlNames.LOGIN.get_template()}, name=UrlNames.LOGIN.name),

                        url(UrlNames.LOGOUT.url_matcher, requires_auth_strict(logout),
                            {'next_page': UrlNames.INDEX.name},
                            name=UrlNames.LOGOUT.name),

                       url(r'^forgot_password/$',
                           requires_noauth_strict(password_reset),
                                    {'post_reset_redirect' : '/forgot_password/mailed/',
                                     'template_name': 'forgot_password/form.html',
                                     'email_template_name': 'forgot_password/email.html',
                                     },
                                    name="forgot_password"),

                            url(r'^forgot_password/mailed/$',
                                password_reset_done,
                                # no requires noauth as this view is just a success message page
                                {'template_name': 'forgot_password/mailed.html'}),

                            #
                       # used by both activation script and forgot passsword
                            #
                            url  (r'^reset_password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                                  password_reset_confirm,
                                  # no requires noauth as user may have figured out password and logged in by then
                                  {'template_name': 'reset_password/form.html',
                                   'set_password_form': ResetPasswordForm,
                                   'post_reset_redirect': '/reset_password/complete/'},
                                  ),

                       url(r'^reset_password/complete/$', password_reset_complete,
                           # no requires noauth as this view is just a success message page
                           {'template_name': 'reset_password/complete.html'}),
)

urlpatterns += patterns(core.views,

                        # For now all hwcentral business urls are consolidated here.
                        # TODO: Move this routing logic to separate urlconfs when making the project more modular

                        UrlNames.ABOUT.create_static_route(),

                        # not a static route as some dynamic redirection is done in the view
                        url(UrlNames.INDEX.url_matcher, dynamic_router, {HttpMethod.GET: index_get},
                            name=UrlNames.INDEX.name),

                        # url(UrlNames.REGISTER.url_matcher, dynamic_router,
                        # {HttpMethod.GET: register_get, HttpMethod.POST: register_post},
                        #     name=UrlNames.REGISTER.name),

                        url(UrlNames.HOME.url_matcher, dynamic_router, {HttpMethod.GET: home_get},
                            name=UrlNames.HOME.name),
                        url(UrlNames.SETTINGS.url_matcher, dynamic_router, {HttpMethod.GET: settings_get},
                            name=UrlNames.SETTINGS.name),

                        url(UrlNames.SUBJECT_ID.url_matcher, dynamic_router, {HttpMethod.GET: subject_id_get},
                            name=UrlNames.SUBJECT_ID.name),
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

                        url(UrlNames.SECURE_STATIC.url_matcher, dynamic_router, {HttpMethod.GET: secure_static_get},
                            name=UrlNames.SECURE_STATIC.name)
                        )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url('^__debug__/', include(debug_toolbar.urls)),
                            )

    urlpatterns += patterns('',
                            # Uncomment the admin/doc line below to enable admin documentation:
                            url('^admin/doc/', include('django.contrib.admindocs.urls')),
                            # Uncomment the next line to enable the admin:
                            url('^admin/', include(admin.site.urls)),
                            )