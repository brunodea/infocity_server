from events.models import EventType, EventKeyword, Event
from django.contrib.gis import admin

admin.site.register(Event, admin.OSMGeoAdmin)
admin.site.register(EventType)
admin.site.register(EventKeyword)
