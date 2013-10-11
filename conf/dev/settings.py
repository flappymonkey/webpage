#encoding=utf8
# Django settings for zhs project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os,sys

import pymongo
if pymongo.version.startswith("2.5"):
    import bson.objectid
    import bson.json_util
    pymongo.objectid = bson.objectid
    pymongo.json_util = bson.json_util
    sys.modules['pymongo.objectid'] = bson.objectid
    sys.modules['pymongo.json_util'] = bson.json_util

curr_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.normpath(os.path.join(curr_path,os.path.pardir))

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

MGDBS = {
    'HOST':'192.168.38.226',
    'PORT':27017,
    'USER':'',
    'PASSWORD':''
}

TOP_RET_NUM = 3
PAGE_RET_NUM = 10
COOKIE_AGE = 86400*30*12
SECKILL_PAGE_RET_NUM = 30
NO_PRICE_WAIT_TIME = 600

APP_ID = '100523811'
APP_KEY = '3887571625470e9c32cd0ec3279dd7d8'
REDIRECT_URI = 'http://ztmhs.maimiaotech.com/auth/login'
SCOPE = 'all'

TAOBAO_APP_KEY = '21635981'
TAOBAO_APP_SECRET = '6d159c2c4ac796a05b5c56ac4bbdc126'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['ztmhs.maimiaotech.com','qq.ztmhs.com', 'www.ztmhs.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = '/home/prd2c/django_project/qq/ztmhs/static/'
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT,'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3ygx9c-rfm*^b78q82dbpt_s27g#q_tglcb&sqd)$-hcz)476%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangomako.middleware.MakoMiddleware',
    'common.exception_middleware.ExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'zhs.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zhs.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT,'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file':{
            'formatter': 'default',
            'class':'logging.FileHandler',
            'filename':  '/tmp/zhs.log',
            },
        'dbfile':{
            'formatter': 'default',
            'class':'logging.FileHandler',
            'filename': '/tmp/zhs_db.log'
        },
        'statfile':{
            'formatter': 'default',
            'class':'logging.FileHandler',
            'filename': '/tmp/zhs_stat.log',
            }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'infolog':{
            'handlers':['file'],
            'level':'INFO',
            'propagate':True,
            },
        'statlog':{
            'handlers':['statfile'],
            'level':'INFO',
            'propagate':True,
            },

        },
    'formatters':{
        'default':{
            'format': '%(asctime)s %(levelname)-2s %(name)s.%(funcName)s:%(lineno)-5d %(message)s'
        }
    }
}


#利用mongodb 自带的connection poll 来管理数据库连接
from pymongo import Connection
from pymongo.errors import AutoReconnect
try:
    mongoConn = Connection(host=MGDBS['HOST'],port=MGDBS['PORT'])
except AutoReconnect,e:
    print "init mongo connection failed.... "
    mongoConn = None
