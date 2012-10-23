from models import EventType, Event
from django.http import HttpResponse

def events(request):
    return HttpResponse('test')
