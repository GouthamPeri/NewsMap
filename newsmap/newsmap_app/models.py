# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    link = models.CharField(max_length=200)
    # guid = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    # pub_date = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='items')


    def __unicode__(self):
        return self.title[:10]
