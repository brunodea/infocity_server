from models import EventType, Event, EventKeyword, EventContextData, EventLike
from django.http import HttpResponse
from django.core.serializers.base import DeserializationError
from django.contrib.gis.geos import GEOSGeometry

from django.utils import simplejson
import jsonhelper
import textretrieval

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
        
        contextdata = generateContextData(request.POST['context_data'])
        contextdata.event = event
        contextdata.save()
        
        response['pk'] = event.pk
    except DeserializationError as error:
        response['response'] = str(error)
        
    #returns a json with an error or an ok and the primary key from the added event.
    return jsonhelper.json_response(response)

def getLikeAction(request, event_id, user_id):
    response = {}
    event = Event.objects.get(pk=event_id)
    if event:
        try:
            event_like = EventLike.objects.get(user_id=user_id,event=event)
            like_action = 0
            if event_like.like == False:
                like_action = 1
        except Exception as e:
            like_action = -1

        response['like_action'] = like_action
    else:
        response['error'] = 'event ' + event_id + ' doest not exits in the database.'
    return jsonhelper.json_response(response)
    
def likeEvent(request, event_id, user_id, like):
    response = {}
    event = Event.objects.get(pk=event_id)
    if event:
        try:
            event_like = EventLike.objects.get(user_id=user_id,event=event)
        except Exception as e:
            event_like = None
        if event_like:
            if like == -1:
                EventLike.objects.remove(event_like)
            else:
                event_like.like = like == 0
                event_like.save()
        elif not like == -1:
            event_like = EventLike(event=event,user_id=user_id,like=like == 0)
            event_like.save()
    
        response['ok'] = 'ok'        
    else:
        response['error'] = 'error: event ' + str(event_id) + ' does not exist.'
    
    return jsonhelper.json_response(response)

def countLikes(event_id):
    event = Event.objects.get(pk=event_id)
    if not event:
        return 0
    likes = EventLike.objects.filter(event=event,like=True)
    return likes.count()

def countDislikes(event_id):
    event = Event.objects.get(pk=event_id)
    if not event:
        return 0
    dislikes = EventLike.objects.filter(event=event,like=False)
    return dislikes.count()

def countLikesDislikes(event_id):
    response['likes'] = countLikes(event_id)
    response['dislikes'] = countDislikes(event_id)
    
    return jsonhelper.json_response(response)

def getEventsWithin(request, latitude, longitude, distance_meters, max_events, context_data):
    """
    Returns a json with all the events within some distance from some location
    and that doesn't have the primary key in the list discard_pks.
    """
    pnt = GEOSGeometry('POINT('+longitude+' '+latitude+')')
    
    cd_dict = contextDataJSONToDict(context_data)
    has_filter = 'filter_eventtype' in cd_dict

    in_contextdata = generateContextData(context_data)
    if has_filter:
        cd_filter = cd_dict['filter_eventtype']
        eventtype_filter = EventType.objects.filter(name=cd_filter)
        if eventtype_filter:
            events = Event.objects.filter(geo_coord__distance_lt=(pnt,float(distance_meters)),
                                          event_type=eventtype_filter)
        else:
            has_filter = False
    
    if not has_filter:
        events = Event.objects.filter(geo_coord__distance_lt=(pnt,float(distance_meters)))
    
        if not str(in_contextdata.from_supplier).lower() == 'filtro':
            events = sort_events_by_relevance([e for e in events], in_contextdata)
       
    response = {'size': len(events)}
    i = 0

    for e in events:
        if i == int(max_events):
            break
        #sends the name string of event_type and the keywords instead of sending
        #their primary keys.
        event_type = EventType.objects.get(pk=e.event_type.pk).name
        keywords = [EventKeyword.objects.get(pk=key.pk).keyword for key in e.keywords.all()]
        json = eval(jsonhelper.toJSON(e))
        json['fields']['event_type'] = event_type
        json['fields']['keywords'] = keywords
        json['fields']['likes'] = countLikes(e.pk)
        json['fields']['dislikes'] = countDislikes(e.pk)
        response['event_'+str(i)] = json
        i += 1
            
    #returns a json with the number of fetched events and with them as well.
    return jsonhelper.json_response(response)

def contextDataJSONToDict(context_data_json):
    cd = context_data_json.encode('utf-8')
    if cd[0] == '"':
        cd = cd[1:-1]
    cd = eval(cd)
    
    return cd

def generateContextData(context_data_json):
    cd = contextDataJSONToDict(context_data_json)
    context_data = EventContextData(place_name=cd['place_name'],place_type=cd['place_type'],
        movement_state=cd['movement_state'],address=cd['address'],on_commute=cd['on_commute'],
        from_supplier=cd['from_supplier'])
    return context_data

def getEventTypes(request):
    response = {}
    types = []
    for t in EventType.objects.all():
        types.append(t.name)
    response['types'] = types
    
    return jsonhelper.json_response(response)

def sort_events_by_relevance(events, in_context):
    query = in_context.relevant_info().lower()
    texts = []
    for e in events:
        try:
            context = EventContextData.objects.get(event=e)
            texts.append((e.pk,(e.relevant_info() + ' ' + context.relevant_info()).lower()))
        except Exception as e:
            pass
    sorted_pks = textretrieval.relevant_texts(texts, query)

    events = []
    for pk in sorted_pks:
        events.append(Event.objects.get(pk=pk))

    return events

