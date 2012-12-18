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

    def relevant_info(self):
        return self.title + ' ' + self.description + ' ' + str(self.event_type) + ' ' + ' '.join(map(str,self.keywords.all()))

class EventContextData(models.Model):
    place_name = models.CharField(max_length=128)
    place_type = models.CharField(max_length=128)
    movement_state = models.CharField(max_length=64)
    on_commute = models.BooleanField()
    address = models.CharField(max_length=1024)
    from_supplier = models.CharField(max_length=64)
    
    event = models.ForeignKey(Event)
    
    def __unicode__(self):
        return '%s (%s)' % (self.place_name.encode('utf-8'),self.place_type.encode('utf-8'))

    def relevant_info(self):
        return self.place_name + ' ' + self.place_type

class EventLike(models.Model):
    event = models.ForeignKey(Event)
    user_id = models.CharField(max_length=512)
    
    like = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.like:
            return 'like'
        else:
            return 'dislike'




