#!/usr/bin/python

"""
WSGI config for baluproject project.
This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.
Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.
"""

import os, sys
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/dmitry/mob-site/python-bin/lib/python3.12/site-packages/django')
sys.path.append('/home/dmitry/mob-site/mob/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mob.settings'

try:
    application = get_wsgi_application()
    sys.stderr.write('WSGI without exception')
except Exception:
    print('handling WSGI exception')
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
