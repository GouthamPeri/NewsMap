from django.views.generic import TemplateView

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home$', views.welcome),
    url(r'^$', TemplateView.as_view(template_name="index.html"))
]