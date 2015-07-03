import django
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from django.contrib import admin

import core
from core.utils.auth_check_wrappers import requires_auth_strict
from core.routing.routers import dynamic_router
from core.routing.urlnames import UrlNames
from core.utils.constants import HttpMethod
from core.views import student_chart_get, subjectroom_chart_get,single_subject_student_chart_get, subject_teacher_subjectroom_chart_get,\
    class_teacher_subjectroom_chart_get,assignment_chart_get, classroom_get
from core.views import index_get, register_post, register_get, home_get, settings_get, subject_get, \
    assignment_post, assignment_get, assignments_get, announcement_get, announcement_post
from hwcentral import settings





# using django's inbuilt auth views for auth-specific tasks
urlpatterns = patterns(django.contrib.auth.views,
                        url(UrlNames.LOGIN.url_matcher, login, {'template_name': UrlNames.LOGIN.get_template()},
                            name=UrlNames.LOGIN.name),
                        url(UrlNames.LOGOUT.url_matcher, requires_auth_strict(logout),
                            {'next_page': UrlNames.INDEX.name},
                            name=UrlNames.LOGOUT.name),
)

urlpatterns += patterns(core.views,

                        # For now all hwcentral business urls are consolidated here.
                        # TODO: Move this routing logic to separate urlconfs when making the project more modular

                        url(r'^$', dynamic_router, {HttpMethod.GET: index_get},
                            name=UrlNames.INDEX.name),

                        UrlNames.ABOUT.create_static_route(),

                        url(UrlNames.REGISTER.url_matcher, dynamic_router,
                            {HttpMethod.GET: register_get, HttpMethod.POST: register_post},
                            name=UrlNames.REGISTER.name),

                        url(UrlNames.HOME.url_matcher, dynamic_router, {HttpMethod.GET: home_get},
                            name=UrlNames.HOME.name),
                        url(UrlNames.SETTINGS.url_matcher, dynamic_router, {HttpMethod.GET: settings_get},
                            name=UrlNames.SETTINGS.name),

                        url(UrlNames.SUBJECT_ID.url_matcher, dynamic_router, {HttpMethod.GET: subject_get},
                            name=UrlNames.SUBJECT_ID.name),
                        url(UrlNames.CLASSROOM_ID.url_matcher, dynamic_router, {HttpMethod.GET: classroom_get},
                            name=UrlNames.CLASSROOM_ID.name),

                        url(UrlNames.ASSIGNMENTS.url_matcher, dynamic_router, {HttpMethod.GET: assignments_get},
                            name=UrlNames.ASSIGNMENTS.name),
                        url(UrlNames.ASSIGNMENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: assignment_get,
                                                                                 HttpMethod.POST: assignment_post},
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

                        url(UrlNames.ANNOUNCEMENT.url_matcher, dynamic_router, {HttpMethod.GET: announcement_get,
                                                                                HttpMethod.POST: announcement_post

                                                                                }, name=UrlNames.ANNOUNCEMENT.name),


                        # url(UrlNames.STUDENT.url_matcher, dynamic_router, {HttpMethod.GET: student_get},
                        # name=UrlNames.STUDENT.name),
                        # url(UrlNames.CLASSROOM.url_matcher, dynamic_router, {HttpMethod.GET: classroom_get},
                        # name=UrlNames.CLASSROOM.name),
                        # url(UrlNames.SCHOOL.url_matcher, dynamic_router, {HttpMethod.GET: school_get},
                        # name=UrlNames.SCHOOL.name)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )

    urlpatterns += patterns('',
                            # Uncomment the admin/doc line below to enable admin documentation:
                            url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                            # Uncomment the next line to enable the admin:
                            url(r'^admin/', include(admin.site.urls)),
                            )