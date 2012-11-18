from models import EventType, Event, EventKeyword
from django.http import HttpResponse
from django.core.serializers.base import DeserializationError
from django.contrib.gis.geos import GEOSGeometry

import jsonhelper

def events(request):
    """
    Key method that delegates the response to another method accordingly some
    request attribute(s).
    """
    event_name = 'generic event type'
    if request.method == 'GET':
        if 'name' in request.GET:
            event_name = request.GET['name']
        else:
            event_name = 'get event type'
    if request.method == 'POST':
        event_name = 'post event type'

    response = jsonhelper.toJSON(EventType(name=event_name))
    return HttpResponse(str(response),'application/json')

def addNewEvent(request):
    """
    Method that adds an event to the spatial database.
    """
    response = {'response':'ok'}
    try:
    
        event_type_name = request.POST['event_type'].encode('utf-8').lower().strip()
        event_type, created = EventType.objects.get_or_create(name=event_type_name)
    
        event_keywords = request.POST['event_keywords'].encode('utf-8')
        event_keywords = event_keywords[1:-1].split(',')
        keywords = []
        for keyword in event_keywords:
            k, created = EventKeyword.objects.get_or_create(keyword=keyword.strip())
            keywords.append(k)

        event_json = eval(request.POST['event'].encode('utf-8'))[0]['fields']

        geo_coord = event_json['geo_coord'].replace(',',' ')
        geo_coord = GEOSGeometry('POINT('+geo_coord+')')

        event = Event(title=event_json['title'],description=event_json['description'],
            pub_date=event_json['pub_date'],geo_coord=geo_coord)
        event.event_type = event_type
        event.save()
        for k in keywords:
            event.keywords.add(k)
        event.save()
    except DeserializationError as error:
        response['response'] = str(error)
    return HttpResponse(str(response),'application/json')

def getEventsWithin(request, latitude, longitude, distance_meters):
    pnt = GEOSGeometry('POINT('+latitude+' '+longitude+')')
    events = Event.objects.filter(geo_coord__distance_lte=(pnt,float(distance_meters)))
    response = {'size': len(events)}
    i = 0
    for e in events:
        event_type = EventType.objects.get(pk=e.event_type.pk).name
        keywords = [EventKeyword.objects.get(pk=key.pk).keyword for key in e.keywords.all()]
        json = eval(jsonhelper.toJSON(e))
        geo_coord = json['fields']['geo_coord']
        json['fields']['event_type'] = event_type
        json['fields']['keywords'] = keywords
        response['event_'+str(i)] = json
    return HttpResponse(str(response),'application/json')









