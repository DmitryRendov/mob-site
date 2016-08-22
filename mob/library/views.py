# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView, ListView
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Article, Category

## Only for debug
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

class ArticleView(TemplateView):
	model = Article
	queryset = Article.objects.all()
	paginate_by = 5
	template_name = "article_details.html"

class CategoryView(TemplateView):
	model = Category
	template_name = "category.html"
