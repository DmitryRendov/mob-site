# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import DetailView, TemplateView, ListView
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from .models import Article, Category

## Only for debug
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

class ArticleDetailView(DetailView):
	model = Article
	template_name = "article_details.html"

class ArticleListView(ListView):
	model = Article
	template_name = "article_list.html"
	paginate_by = getattr(settings, 'LIBRARY_PAGESIZE')

class CategoryView(TemplateView):
	model = Category
	template_name = "category_list.html"
