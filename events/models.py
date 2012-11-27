#-*- coding: utf8 -*-

from django.contrib.gis.db import models

class EventType(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.name.encode('utf-8'))

class EventKeyword(models.Model):
    keyword = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.keyword.encode('utf-8'))

class EventContextData(models.Model):
    place_name = models.CharField(max_length=128)
    place_type = models.CharField(max_length=128)
    movement_state = models.CharField(max_length=64)
    on_commute = models.BooleanField(initial=False)
    address = models.CharField(max_length=1024)
    
    def __unicode__(self):
        return '%s (%s)' % (self.place_name.encode('utf-8'),self.place_type.encode('utf-8'))

class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    event_type = models.ForeignKey(EventType)
    pub_date = models.DateTimeField('date published')
    keywords = models.ManyToManyField(EventKeyword)

    #GeoDjango específico.
    geo_coord = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.title.encode('utf-8') + " " + str(self.geo_coord)
