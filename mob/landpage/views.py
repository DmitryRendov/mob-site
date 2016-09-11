# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import TemplateView
from django.utils.translation import ugettext, ugettext_lazy as _

from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

## Only for debug
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

@method_decorator(csrf_protect, name='dispatch')
class LandPageView(TemplateView):
	template_name = "main.html"
