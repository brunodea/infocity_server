from django.conf.urls import patterns, include, url

urlpatterns = patterns('events.views',
    url(r'^events/$', 'events'),
    url(r'^add/$', 'addNewEvent'),
    url(r'^getWithin/(?P<latitude>-?\d+(\.\d+)?)/(?P<longitude>-?\d+(\.\d+)?)' +
        '/(?P<distance_meters>\d+)/$', 'getEventsWithin'),
)
