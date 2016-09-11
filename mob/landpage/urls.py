"""Landing page URL Configuration
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.LandPageView.as_view(),
        name='index'),
]
