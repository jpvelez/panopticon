import os
import sys

# Add project dir to the path.
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Add django settings to server env.
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Tell apache to load app as a separate process that handles incoming
# HTTP requests.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()