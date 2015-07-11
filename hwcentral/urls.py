import django
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login, password_reset_confirm, password_reset_done, password_reset, \
    password_reset_complete
from django.contrib import admin

import core
from core.forms.password import ForgotPasswordForm
from core.utils.auth_check_wrappers import requires_auth_strict
from core.routing.routers import dynamic_router
from core.routing.urlnames import UrlNames
from core.utils.constants import HttpMethod
from core.views import home_get, settings_get, announcement_get, announcement_post, assignment_get, \
    student_chart_get, \
    subjectroom_chart_get,single_subject_student_chart_get, subject_teacher_subjectroom_chart_get, \
    class_teacher_subjectroom_chart_get, assignment_chart_get, password_get, password_post, \
    secure_static_get, subject_id_get, classroom_id_get, assignment_id_get, assignment_id_post, \
    standard_assignment_chart_get
from hwcentral import settings


# using django's inbuilt auth views for auth-specific tasks
urlpatterns = patterns(django.contrib.auth.views,

                        url(UrlNames.LOGIN.url_matcher, login, {'template_name': UrlNames.LOGIN.get_template()},
                            name=UrlNames.LOGIN.name),

                        url(UrlNames.LOGOUT.url_matcher, requires_auth_strict(logout),
                            {'next_page': UrlNames.INDEX.name},
                            name=UrlNames.LOGOUT.name),
                       url(r'^forgot_password/$',
                                   password_reset,
                                    {'post_reset_redirect' : '/forgot_password/mailed/',
                                     'template_name' : 'password/forgot_password_form.html',
                                     'email_template_name':'password/forgot_password_email.html'},
                                    name="forgot_password"),

                            url(r'^forgot_password/mailed/$',
                                    password_reset_done,
                                {'template_name': 'password/forgot_password_done.html'}),

                            url  (r'^forgot_password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                                 password_reset_confirm,
                                 {'template_name' : 'password/forgot_password_confirm.html',
                                  'set_password_form':ForgotPasswordForm,
                                  'post_reset_redirect':'/complete/' },
                                    ),

                            url(r'^complete/$',password_reset_complete,
                                {'template_name': 'password/forgot_password_complete.html'}),
)

urlpatterns += patterns(core.views,

                        # For now all hwcentral business urls are consolidated here.
                        # TODO: Move this routing logic to separate urlconfs when making the project more modular

                        UrlNames.INDEX.create_static_route(),
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
                        url(UrlNames.CLASSROOM_ID.url_matcher, dynamic_router, {HttpMethod.GET: classroom_id_get},
                            name=UrlNames.CLASSROOM_ID.name),

                        url(UrlNames.ASSIGNMENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: assignment_id_get,
                                                                                 HttpMethod.POST: assignment_id_post},
                            name=UrlNames.ASSIGNMENT_ID.name),

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