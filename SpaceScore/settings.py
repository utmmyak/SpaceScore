"""
Django settings for SpaceScore project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys

from secrets import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = (('Noah', 'nlowenthal@comcast.net'))

MANAGERS = ADMINS

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'CongressScore',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'PIL',
    'haystack',
    'django_evercookie',
    'localflavor',
    'xlwt',
    'xlsxwriter',
#    'crispy_forms',
#    'csvimport',
    'import_export',
    'reversion',
#    'crispy_forms',
    'debug_toolbar',
#    'south',
    #'corsheaders',
    #'xadmin',
    'sorl.thumbnail'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_dont_vary_on.middleware.RemoveUnneededVaryHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    #'django.contrib.csrf.middleware.CsrfViewMiddleware',
    #'django.contrib.csrf.middleware.CsrfResponseMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'SpaceScore.urls'

WSGI_APPLICATION = 'SpaceScore.wsgi.application'

#CORS_ORIGIN_WHITELIST = ('0.0.0.0', 'localhost','127.0.0.1',)
#CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SpaceScoreDB',
        'USER': 'SpaceScore',
        'PASSWORD': 'noahl',
        'TEST_MIRROR': 'test',
        'HOST': '',
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'TestDB',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '',
         # ... plus some other settings
    }
}

SOCIAL_AUTH_UID_LENGTH = 255

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'INCLUDE_SPELLING': True
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '0.0.0.0:11211',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                "django.template.context_processors.request",
                'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]
ADMIN_MEDIA_PREFIX = '/static/admin/'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

DEFAULT_CHARSET = 'utf-8'

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'https://static.spacescore.com/'
STATIC_ROOT = BASE_DIR+'/static'
MEDIA_URL = "https://static.spacescore.com/media/"
MEDIA_ROOT = BASE_DIR+'/static/media'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'utmmyak@gmail.com'
EMAIL_HOST_PASSWORD = 'googleHam42'
EMAIL_PORT = 587
INTERNAL_IPS = ("208.167.254.244",)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console', 'logfile'],
            'propagate': True,
            'level':'INFO',
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'SpaceScore': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

# GRAPPELLI SETTING EXTENSIONS
# REMOVE IF WE ARE NOT USING GRAPPELLI
GRAPPELLI_ADMIN_TITLE = "SpaceScore"