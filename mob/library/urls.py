"""Landing page URL Configuration
"""
from django.conf.urls import url
from library import views

app_name = 'mob'

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ArticleListView.as_view(),
        name='article_list'
    ),

    url(
        regex=r'^(?P<slug>[-\w]+)/$',
        view=views.ArticleDetailView.as_view(),
        name='article_detail'
    ),

    url(
        regex=r'^page/(?P<page>\d+)/$',
        view=views.ArticleListView.as_view(),
        name='article_list'
    ),

    url(
        regex=r'^categories/$',
        view=views.CategoryView.as_view(),
        name='category_list'
    ),
]
