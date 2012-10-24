from django.core.serializers import serialize
from django.db import models
from django.db.models.query import QuerySet

def toJSON(obj):
    if isinstance(obj, QuerySet):
        pass
    elif isinstance(obj, models.Model):
        set_obj = [obj]
    else:
        return None

    ser = serialize('json',set_obj)
    set_str = ser[1:len(ser)-1]
    return set_str
