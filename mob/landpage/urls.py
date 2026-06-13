"""Landing page URL Configuration
"""
from django.conf.urls import url
from . import views

app_name = 'mob'

urlpatterns = [
    url(r'^$',
        views.LandPageView.as_view(),
        name='index'),
]
