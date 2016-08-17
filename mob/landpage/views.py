# coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

## Only for debug
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# end of debug

def index(request):
    args = {}
    args.update(csrf(request))
    return render_to_response("main.html",
                              context_instance=RequestContext(request))
def layout(request):
    args = {}
    args.update(csrf(request))
    return render_to_response("layout.html",
                              context_instance=RequestContext(request))