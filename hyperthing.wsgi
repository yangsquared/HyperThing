import os
import sys
#print >> sys.stderr, rdflib.__version__
import logging

logging.basicConfig(filename='/var/log/render/messages.log',level=logging.ERROR)

sys.path.append('/var/djangoapp/src')

os.environ['DJANGO_SETTINGS_MODULE'] = 'hyperthing.settings'
sys.stdout = sys.stderr

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()