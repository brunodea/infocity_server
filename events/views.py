from models import EventType, Event, EventKeyword, EventContextData
from django.http import HttpResponse
from django.core.serializers.base import DeserializationError
from django.contrib.gis.geos import GEOSGeometry

from django.utils import simplejson
import jsonhelper

def addNewEvent(request):
    """
    Method that adds an event to the spatial database.
    """
    response = {'response':'ok'}
    try:
        #event_type and event_keywords come as names, not IDs. So we need first
        #to get their primary keys so we can save the Event properly.
        event_type_name = request.POST['event_type'].encode('utf-8').lower().strip()
        event_type, created = EventType.objects.get_or_create(name=event_type_name)
    
        event_keywords = request.POST['event_keywords'].encode('utf-8')
        event_keywords = event_keywords[1:-1].split(',')
        keywords = []
        for keyword in event_keywords:
            k, created = EventKeyword.objects.get_or_create(keyword=keyword.strip())
            keywords.append(k)

        #gets what is interesting about the Event and makes it compatible 
        #with the server's format.
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
        
        cd = eval(request.POST['context_data'].encode('utf-8'))
        contextdata = EventContextData(place_name=cd['place_name'],place_type=cd['place_type'],
            movement_state=cd['movement_state'],address=cd['address'],on_commute=cd['on_commute'],
            event=event)
        contextdata.save()
        
        response['pk'] = event.pk
    except DeserializationError as error:
        response['response'] = str(error)
        
    #returns a json with an error or an ok and the primary key from the added event.
    return jsonhelper.json_response(response)

def getEventsWithin(request, latitude, longitude, distance_meters, context_data):
    """
    Returns a json with all the events within some distance from some location
    and that doesn't have the primary key in the list discard_pks.
    """
    pnt = GEOSGeometry('POINT('+longitude+' '+latitude+')')
    #creates the list of not wanted primary keys.
    events = Event.objects.filter(geo_coord__distance_lt=(pnt,float(distance_meters)))
    
    
    cd = eval(context_data.encode('utf-8'))
    curr_contextdata = EventContextData(place_name=cd['place_name'],place_type=cd['place_type'],
        movement_state=cd['movement_state'],address=cd['address'],on_commute=cd['on_commute'])
    
    response = {'size': len(events)}
    i = 0

    for e in events:
        contextdata = EventContextData.objects.get(event=e)
        if not eventIsRelevant(e, contextdata):
            continue
    
        response[str(i)] = str(e)
        #sends the name string of event_type and the keywords instead of sending
        #their primary keys.
        event_type = EventType.objects.get(pk=e.event_type.pk).name
        keywords = [EventKeyword.objects.get(pk=key.pk).keyword for key in e.keywords.all()]
        json = eval(jsonhelper.toJSON(e))
        json['fields']['event_type'] = event_type
        json['fields']['keywords'] = keywords
        response['event_'+str(i)] = json
        i += 1
            
    #returns a json with the number of fetched events and with them as well.
    return jsonhelper.json_response(response)

def getEventTypes(request):
    response = {}
    types = []
    for t in EventType.objects.all():
        types.append(t.name)
    response['types'] = types
    
    return jsonhelper.json_response(response)

def eventIsRelevant(event, context_data):
    return True


