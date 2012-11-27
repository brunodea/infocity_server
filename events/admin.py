from events.models import EventType, EventKeyword, Event, EventContextData
from django.contrib.gis import admin

admin.site.register(Event, admin.OSMGeoAdmin)
admin.site.register(EventType)
admin.site.register(EventKeyword)
admin.site.register(EventContextData)
