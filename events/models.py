#-*- coding: utf8 -*-

from django.contrib.gis.db import models

class EventType(models.Model):
    name = models.CharField(max_length=64)

class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    event_type = models.ForeignKey(EventType)
    pub_date = models.DateTimeField('date published')
    
    #GeoDjango específico.
    geo_coord = models.PointField()
    objects = models.GeoManager()
