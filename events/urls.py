from django.conf.urls import patterns, include, url

urlpatterns = patterns('events.views',
    url(r'^add/$', 'addNewEvent'),
    url(r'^getWithin/(?P<latitude>-?\d+(\.\d+)?)/(?P<longitude>-?\d+(\.\d+)?)' +
        '/(?P<distance_meters>\d+(\.\d+)?)/(?P<context_data>.*)$', 'getEventsWithin'),
    url(r'^eventTypes/$', 'getEventTypes'),
)
