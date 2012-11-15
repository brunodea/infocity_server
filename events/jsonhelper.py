from django.core.serializers import serialize, deserialize
from django.db import models
from django.db.models.query import QuerySet

def toJSON(obj):
    if isinstance(obj, QuerySet):
        pass
    elif isinstance(obj, models.Model):
        set_obj = [obj]
    else:
        return None

    ser = serialize('json',set_obj,ensure_ascii=False)
    set_str = ser[1:len(ser)-1]
    return set_str

def fromJSON(obj, ignore_non_existent):
    return deserialize('json', obj, ensure_ascii=False,
        ignorenonexistent=ignore_non_existent)
