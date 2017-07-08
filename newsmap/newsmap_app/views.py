# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import time
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from models import *
from serializers import *
import feedparser
import pprint

city_urls = {'Mumbai' : -2128838597,'Delhi' : -2128839596, 'Banglore' : -2128833038, 'Hyderabad' : -2128816011, 'Chennai' : 2950623,
    'Ahemdabad' : -2128821153, 'Allahabad' : 3947060, 'Bhubaneswar' : 4118235, 'Coimbatore' :7503091, 'Gurgaon' : 6547154,
    'Guwahati' : 4118215, 'Hubli' : 3942695, 'Kanpur' : 3947067, 'Kolkata' : -2128830821, 'Ludhiana' : 3947051,
    'Mangalore' : 3942690, 'Mysore' : 3942693, 'Noida' : 8021716, 'Pune' : -2128821991, 'Goa' : 3012535,
    'Chandigarh' : -2128816762, 'Lucknow' : -2128819658, 'Patna' : -2128817995, 'Jaipur' : 3012544,
    'Nagpur' : 442002, 'Rajkot' : 3942663, 'Ranchi' : 4118245, 'Surat' : 3942660, 'Vadodara' : 3942666,
    'Varanasi' : 3947071, 'Thane' : 3831863, 'Thiruvananthapuram' : 878156304
}


def extract_feed(city_name):
    url = "http://timesofindia.indiatimes.com/rssfeeds/" + str(city_urls[city_name]) + ".cms"
    feed = feedparser.parse(url)
    if not City.objects.filter(name=city_name).exists():
        city = City.objects.create(name=city_name, link=url)
    else:
        city = City.objects.get(name=city_name)
    for item in feed['items']:
        news_item = {}
        news_item['title'] = item['title']
        news_item['description'] = item['summary']
        news_item['link'] = item['link']
        news_item['pub_date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
        news_item['city'] = city
        NewsItem.objects.create(**news_item)


def welcome(request):
    print City.objects.all().delete()
    for city in city_urls.keys():
        extract_feed(city)
    return HttpResponse("Welcome to NewsMap, Sync finished")


class RetrieveNewsItemsJSON(ListAPIView):
    serializer_class = NewsItemSerializer
    queryset = NewsItem.objects.all()

    def get_queryset(self):
        city = City.objects.get(pk=self.kwargs['pk'])
        return self.queryset.filter(city=city)


def get_city_coords(request):
    city_coords = {}
    return JsonResponse(json.dumps(city_coords), safe=False)


@csrf_exempt
def get_news(request):
    if request.method == 'POST':
        cities = request.POST.getlist('cities[]')
        data = {}
        if len(cities):
            queryString = 'list(NewsItem.objects.filter('
            for i in range(0, len(cities) - 1):
                queryString += 'Q(city__name__startswith=' + repr(cities[i]) + ')|'
            else:
                queryString += 'Q(city__name__startswith=' \
                               + repr(cities[len(cities) - 1]) \
                               + ')).values("city__name", "pub_date", "title", "description", "link").order_by("-pub_date"))'

            print queryString
            data['items'] = eval(queryString)
            for i in range(len(data['items'])):
                data['items'][i]['pub_date'] = data['items'][i]['pub_date'].strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse(json.dumps(data), safe=False)

