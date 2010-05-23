from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       
                       url(r'^stream/(?P<gid>\d+)/$', 'constellation.views.stream',
                           name="group_stream"),
                       url(r'^links/(?P<gid>\d+)/$', 'constellation.views.links',
                           name="group_links"),
                       url(r'^group/(?P<gid>\d+)/$', 'constellation.views.group',
                           name="group"),

                       )