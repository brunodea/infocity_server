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
