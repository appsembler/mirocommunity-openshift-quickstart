#!/usr/bin/env python
import urlparse
import os
import sys

#########
# PATHS #
#########

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OPENSHIFT_DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR')
OPENSHIFT_REPO_DIR = os.environ.get('OPENSHIFT_REPO_DIR')

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

sys.path.insert(0, PROJECT_ROOT)

from test_project.settings import *

#############
# DATABASES #
#############

# TODO: clean up this code so it's less verbose

DATABASES = {}
if 'OPENSHIFT_MYSQL_DB_URL' in os.environ:
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))

    DATABASES['default'] = {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        }
elif 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    url = urlparse.urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))

    DATABASES['default'] = {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['OPENSHIFT_APP_NAME'],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
        }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }



# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

if 'OPENSHIFT_REPO_DIR' in os.environ:
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
else:
    STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

if 'OPENSHIFT_DATA_DIR' in os.environ:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
else:
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(OPENSHIFT_DATA_DIR, 'whoosh_index'),
        }
    }


DEPLOYER_APPS = (
        'django.contrib.staticfiles',
        'deployer_utils',
        )
INSTALLED_APPS += DEPLOYER_APPS

TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.static',
        )


DEBUG = True
