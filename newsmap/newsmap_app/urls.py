from django.views.generic import TemplateView

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home$', views.welcome),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api/(?P<pk>[0-9]+)/$', views.RetrieveNewsItemsJSON.as_view()),
    url(r'^api/news/$', views.get_news),
    url(r'^newsitems.html', TemplateView.as_view(template_name="newsitems.html")),
    url(r'^api/coords/$', views.get_city_coords)
]