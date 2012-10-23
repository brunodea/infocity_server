from models import EventType, Event
from django.http import HttpResponse

def events(request):
    """
    Key method that delegates the response to another method accordingly some
    request attribute(s).
    """
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    return HttpResponse('test')
