from rest_framework.serializers import ModelSerializer

from models import *


class NewsItemSerializer(ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ['title', 'description', 'link']