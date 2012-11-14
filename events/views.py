from models import EventType, Event
from django.http import HttpResponse
from django.core.serializers.base import DeserializationError

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
        items = jsonhelper.fromJSON(request.POST['event'],False)
        for item in items:
            item.save()
    except DeserializationError as error:
        response['response'] = str(error)
    return HttpResponse(str(response),'application/json')
