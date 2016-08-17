# coding=utf-8
from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

## Only for debug
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

@csrf_protect
def index(request):
    args = {}
    return render(request, "main.html", args)

@csrf_protect
def layout(request):
    args = {}
    return render(request, "layout.html", args)