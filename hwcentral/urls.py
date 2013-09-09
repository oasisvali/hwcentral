from django.conf.urls import patterns, include, url

import core
from core.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),	
	)

urlpatterns += patterns(core.views, 

	# For now all hwcentral business urls are consolidated here. Move this routing logic to seperate urlconfs when making the project more modular
    url(r'^$', land, name='land'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^classroom(?:/(\S+))?/$', classroom, name='classroom'),
    url(r'^hw(?:/(\S+))?/$', hw, name='hw'),
    url(r'^submisssion(?:/(\S+))?/$', submission, name='submission'),
    url(r'^user(?:/(\S+))?/$', user, name='user'),
    url(r'^school(?:/(\S+))?/$', school, name='school'),
    url(r'^board(?:/(\S+))?/$', board, name='board'),

    # Later add topic and subject based views (eg. for listing all publicly available assignments?)
	)
