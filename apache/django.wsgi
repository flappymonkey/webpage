import os
import sys
sys.path.append('/home/ops')
sys.path.append('/home/ops/webpage')
sys.path.append('/home/ops/webpage/zhs')
os.environ['DJANGO_SETTINGS_MODULE'] = 'zhs.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
