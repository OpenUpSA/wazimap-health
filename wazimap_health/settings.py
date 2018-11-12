"""
Django settings for wazimap_health project.

Generated by 'django-admin startproject' using Django 1.9.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
import os
import dj_database_url
from wazimap.settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'HEALTH_SECRET_KEY', 'xf&mewbq*dp4ul-m^!-)+20e2i_&!u@eablvqln08e3@r(ec3e')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('HEALTH_DEBUG', 'true') == 'true'

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'wazimap_health.urls'

# Application definition
INSTALLED_APPS = [
    'wazimap_health', 'rest_framework', 'django.contrib.postgres',
    'django_admin_hstore_widget', 'elasticapm.contrib.django'
] + INSTALLED_APPS

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'elasticapm.contrib.django.middleware.TracingMiddleware',
    'elasticapm.contrib.django.middleware.Catch404Middleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
) + MIDDLEWARE_CLASSES

TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth',
                               ) + TEMPLATE_CONTEXT_PROCESSORS

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://wazimap_health:wazimap_health@10.186.210.252/wazimap_health')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
WAZIMAP['ga_tracking_id'] = 'UA-93649482-12'
WAZIMAP['profile_builder'] = 'wazimap_health.profiles.health.get_profile'
WAZIMAP['default_profile'] = 'youth'
WAZIMAP['geodata'] = 'wazimap_health.geo.GeoData'
WAZIMAP['geometry_data'] = {}
WAZIMAP['default_geo_version'] = '2011'
WAZIMAP['name'] = 'Department of Health'
WAZIMAP['url'] = 'http://wazimap-health.openup.org.za'
WAZIMAP['country_code'] = 'ZA'
WAZIMAP['latest_release_year'] = '2016'
WAZIMAP['primary_dataset_name'] = 'Census and Community Survey'
WAZIMAP['available_release_years'] = {
    # Release years with data for geo_levels.
    # Only specify geo_levels with limited releases.
    # Other geo_levels have data for all releases.
    'ward': [2011]
}
WAZIMAP['levels'] = {
    'country': {
        'plural': 'countries',
        'children': ['province', 'district', 'municipality', 'point'],
    },
    'province': {
        'children': ['district', 'municipality', 'point'],
    },
    'district': {
        'children': ['municipality', 'point'],
    },
    'municipality': {
        'children': ['point']
    },
    'point': {
        'children': []
    },
}

WAZIMAP['mapit'] = {
    'generations': {
        '2011': '1',
        '2016': '2',
        None: '1',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MAPIT_LOCATION_URL = "https://mapit.code4sa.org/point/4326/"

LOGSTASH_URL = os.environ.get('LOGSTASH_URL', '')
APM_SERVER_URL = os.environ.get('APM_SERVER_URL', '')

ELASTIC_APM = {'SERVICE_NAME': 'Wazimap Health', 'SERVER_URL': APM_SERVER_URL}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.TCPLogstashHandler',
            'host': LOGSTASH_URL,
            'port': 5959,
            'version': 1,
            'message_type': 'logstash',
            'fqdn': False,
            'tags': ['Wazimap Health']
        },
        'elasticapm': {
            'level': 'INFO',
            'class': 'elasticapm.contrib.django.handlers.LoggingHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django': {
            'handlers': ['elasticapm', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.template': {
            'handlers': ['elasticapm', 'console'],
            'level': 'ERROR',
        },
        'wazimap': {
            'handlers': ['elasticapm', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    }
}
