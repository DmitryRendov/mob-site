"""Landing page URL Configuration
"""
from django.conf.urls import url
from library import views

urlpatterns = [
    url(r'^$',
        views.ArticleView.as_view(),
        name='article_index'
    ),
    url (r'^categories/$',
        views.CategoryView.as_view(),
        name='article_category_list'
    ),
]
