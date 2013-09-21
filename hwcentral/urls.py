import django
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login

import core
from core.modules.constants import UrlNames, HttpMethod

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from core.views import static_router, redirect_router, dynamic_router, register_get, home_get, register_post

admin.autodiscover()

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)

# using django's inbuilt auth views for auth-specific tasks
urlpatterns += patterns(django.contrib.auth.views,
                        url(UrlNames.LOGIN.toUrlMatcher(), login, {'template_name': 'login.html'},
                            name=UrlNames.LOGIN.name),
                        url(UrlNames.LOGOUT.toUrlMatcher(), logout, {'next_page': UrlNames.SITE_ANCHOR.toUrl()},
                            name=UrlNames.LOGOUT.name),
)

urlpatterns += patterns(core.views,

                        # For now all hwcentral business urls are consolidated here.
                        # TODO: Move this routing logic to separate urlconfs when making the project more modular
                        # TODO: strings bad. move to constants

                        url(r'^$', static_router, {'template': 'index.html'}, name=UrlNames.INDEX.name),

                        url(UrlNames.NEWS.toUrlMatcher(), static_router, {'template': 'news.html'}, name=UrlNames.NEWS.name),
                        url(UrlNames.CONTACT.toUrlMatcher(), static_router, {'template': 'contact.html'}, name=UrlNames.CONTACT.name),
                        url(UrlNames.ABOUT.toUrlMatcher(), static_router, {'template': 'about.html'}, name=UrlNames.ABOUT.name),

                        # keeping this view for now instead of just using index everywhere as inde doesn't have a good urlMatcher
                        url(UrlNames.SITE_ANCHOR.toUrlMatcher(), redirect_router, {'target_view_name': 'index'}, name=UrlNames.SITE_ANCHOR.name),

                        url(UrlNames.HOME.toUrlMatcher(), dynamic_router, {HttpMethod.GET: home_get}, name=UrlNames.HOME.name),
                        url(UrlNames.REGISTER.toUrlMatcher(), dynamic_router, {HttpMethod.GET: register_get, HttpMethod.POST: register_post}, name=UrlNames.REGISTER.name)

                        #url(r'^classroom(?:/(\S+))?/$', classroom, name='classroom'),
                        #url(r'^hw(?:/(\S+))?/$', hw, name='hw'),
                        #url(r'^submission(?:/(\S+))?/$', submission, name='submission'),
                        #url(r'^user(?:/(\S+))?/$', user, name='user'),
                        #url(r'^school(?:/(\S+))?/$', school, name='school'),
                        #url(r'^board(?:/(\S+))?/$', board, name='board'),
                        #url(UrlNames.REGISTER.toUrlMatcher(), dynamic_router,
                        #    {HttpMethod.GET: register_get, HttpMethod.POST: register_post}, name=UrlNames.REGISTER.name),
                        #url(UrlNames.LOGOUT.toUrlMatcher(), requires_auth_strict(dynamic_router), {HttpMethod.POST: logout},
                        #    name=UrlNames.LOGOUT.name),

                        # Later add topic and subject based views (eg. for listing all publicly available assignments?)
)
