from django.conf.urls import patterns, include, url

urlpatterns = patterns('events.views',
    url(r'^add/$', 'addNewEvent'),
    url(r'^getWithin/(?P<latitude>-?\d+(\.\d+)?)/(?P<longitude>-?\d+(\.\d+)?)' +
        '/(?P<distance_meters>\d+(\.\d+)?)/(?P<max_events>\d+)/(?P<context_data>.*)$', 'getEventsWithin'),
    url(r'^eventTypes/$', 'getEventTypes'),
    url(r'^likeEvent/(?P<event_id>\d+)/(?P<user_id>.+)/(?P<like>-?\d)/$',
        'likeEvent'),
    url(r'^getLikeAction/(?P<event_id>\d+)/(?P<user_id>.+)/$', 'getLikeAction'),
    url(r'^countLikesDislikes/(?P<event_id>\d+)/$', 'countLikesDislikes'),
)
