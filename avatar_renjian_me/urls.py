# coding=UTF8
from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'avatar_renjian_me.core.views.indexRequest'),
    (r'^error/$', 'avatar_renjian_me.core.views.error'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debugmedia/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/arthur/workspace/renjian-avatar/avatar_renjian_me/media'}),
    )