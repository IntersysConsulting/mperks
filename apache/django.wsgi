import os, sys

path = '/srv/www/htdocs/mperks/catalina'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'catalina.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

