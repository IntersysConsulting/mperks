import os, sys
sys.path.append('/home/ubuntu/socialmedia')
os.environ['DJANGO_SETTINGS_MODULE'] = 'socialmedia.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
