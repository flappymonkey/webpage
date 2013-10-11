import os
import sys
sys.path.append('/home/ops')
sys.path.append('/home/ops/webpage')
sys.path.append('/home/ops/webpage/taohulu')
os.environ['DJANGO_SETTINGS_MODULE'] = 'taohulu.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
