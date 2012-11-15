#-*- coding: utf8 -*-

from django.contrib.gis.db import models

class EventType(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.name)

class EventKeyword(models.Model):
    keyword = models.CharField(max_length=128)

    def __unicode__(self):
        return str(self.keyword)

class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    event_type = models.ForeignKey(EventType)
    pub_date = models.DateTimeField('date published')
    keywords = models.ManyToManyField(EventKeyword)

    #GeoDjango específico.
    geo_coord = models.PointField()
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.title + " " + str(self.geo_coord)
            
