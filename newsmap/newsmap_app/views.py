# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import time

from dateutil import parser
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from models import *
import datetime
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
        news_item['pub_date'] = str(parser.parse(item['published']) + datetime.timedelta(hours=5, minutes=30))
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
    city_coords = {'Mumbai': {'lat': 19.0760, 'lng': 72.8777}, 'Delhi': {'lat': 28.7041, 'lng': 77.1025},
                   'Banglore': {'lat': 12.9716, 'lng': 77.5946}, 'Hyderabad': {'lat': 17.3850, 'lng': 78.4867},
                   'Chennai': {'lat': 13.0827, 'lng': 80.2707}, 'Ahemdabad': {'lat': 23.0225, 'lng': 72.5714},
                   'Allahabad': {'lat': 25.4358, 'lng': 81.8463}, 'Bhubaneswar': {'lat': 20.2961, 'lng': 85.8245},
                   'Coimbatore': {'lat': 11.0168, 'lng': 76.9558}, 'Gurgaon': {'lat': 28.4595, 'lng': 77.0266},
                   'Guwahati': {'lat': 26.1445, 'lng': 91.7362}, 'Hubli': {'lat': 15.3647, 'lng': 75.1240},
                   'Kanpur': {'lat': 26.4499, 'lng': 80.3319}, 'Kolkata': {'lat': 22.5726, 'lng': 88.3639},
                   'Ludhiana': {'lat': 30.9010, 'lng': 75.8573}, 'Mangalore': {'lat': 12.9141, 'lng': 74.8560},
                   'Mysore': {'lat': 12.2958, 'lng': 76.6394}, 'Noida': {'lat': 28.5355, 'lng': 77.3910},
                   'Pune': {'lat': 18.5204, 'lng': 73.8567}, 'Goa': {'lat': 15.2993, 'lng': 74.1240},
                   'Goa': {'lat': 15.2993, 'lng': 74.1240}, 'Chandigarh': {'lat': 30.7333, 'lng': 76.7794},
                   'Lucknow': {'lat': 26.8467, 'lng': 80.9462}, 'Patna': {'lat': 25.5941, 'lng': 85.1376},
                   'Jaipur': {'lat': 26.9124, 'lng': 75.7873}, 'Nagpur': {'lat': 21.1458, 'lng': 79.0882},
                   'Rajkot': {'lat': 22.3039, 'lng': 70.8022}, 'Surat': {'lat': 21.1702, 'lng': 72.8311},
                   'Vadodara': {'lat': 22.3072, 'lng': 73.1812}, 'Varanasi': {'lat': 25.3176, 'lng': 82.9739},
                   'Thane': {'lat': 19.2183, 'lng': 72.9781}, 'Thiruvananthapuram': {'lat': 8.5241, 'lng': 76.9366}
                  }

    return JsonResponse(json.dumps(city_coords), safe=False)


@csrf_exempt
def get_news(request, page):
    page = int(page)
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
                               + ')).values("city__name", "pub_date", "title", "description", "link")' \
                                 '.order_by("-pub_date")[page:page+10])'

            print queryString
            data['items'] = eval(queryString)
            for i in range(len(data['items'])):
                data['items'][i]['pub_date'] = data['items'][i]['pub_date'].strftime("%Y-%m-%d %H:%M:%S")

    print data
    return JsonResponse(json.dumps(data), safe=False)

