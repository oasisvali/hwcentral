import django
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from django.contrib import admin

import core.views
from core.modules.auth_check_wrappers import requires_auth_strict
from core.modules.constants import HttpMethod
from core.routing.routers import dynamic_router
from core.routing.urlnames import UrlNames
from core.views import register_get, home_get, register_post, index_get, student_get, subject_get, classroom_get, \
    school_get, settings_get, assignment_get, test_get, assignment_post


admin.autodiscover()

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)

# using django's inbuilt auth views for auth-specific tasks
urlpatterns += patterns(django.contrib.auth.views,
                        url(UrlNames.LOGIN.url_matcher, login, {'template_name': UrlNames.LOGIN.template},
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
                        url(UrlNames.HOME.url_matcher, dynamic_router, {HttpMethod.GET: home_get},
                            name=UrlNames.HOME.name),

                        UrlNames.NEWS.create_static_route(),
                        UrlNames.CONTACT.create_static_route(),
                        UrlNames.ABOUT.create_static_route(),

                        url(UrlNames.REGISTER.url_matcher, dynamic_router,
                            {HttpMethod.GET: register_get, HttpMethod.POST: register_post},
                            name=UrlNames.REGISTER.name),

                        url(UrlNames.SUBJECT.url_matcher, dynamic_router, {HttpMethod.GET: subject_get},
                            name=UrlNames.SUBJECT.name),

                        url(UrlNames.SETTINGS.url_matcher, dynamic_router, {HttpMethod.GET: settings_get},
                            name=UrlNames.SETTINGS.name),
                        url(UrlNames.TEST.url_matcher, dynamic_router, {HttpMethod.GET: test_get},
                            name=UrlNames.TEST.name),

                        url(UrlNames.ASSIGNMENT.url_matcher, dynamic_router, {HttpMethod.GET: assignment_get},
                            name=UrlNames.ASSIGNMENT.name),
                        url(UrlNames.ASSIGNMENT_ID.url_matcher, dynamic_router, {HttpMethod.GET: assignment_get,
                                                                                 HttpMethod.POST: assignment_post},
                            name=UrlNames.ASSIGNMENT_ID.name),

                        url(UrlNames.STUDENT.url_matcher, dynamic_router, {HttpMethod.GET: student_get},
                            name=UrlNames.STUDENT.name),
                        url(UrlNames.CLASSROOM.url_matcher, dynamic_router, {HttpMethod.GET: classroom_get},
                            name=UrlNames.CLASSROOM.name),
                        url(UrlNames.SCHOOL.url_matcher, dynamic_router, {HttpMethod.GET: school_get},
                            name=UrlNames.SCHOOL.name),
)
