"""Django base settings for awesome directory setup.
"""
import sys
import os
import yaml

# Django docs say this line is redundant, but we want to extend
# variables like TEMPLATE_CONTEXT_PROCESSORS, so we are going to be
# rebels and import this anyway
from django.conf.global_settings import *

# Get the project path,
PROJECT_ROOT = os.path.realpath(os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
)))

# Turn on debugging statements when using runserver.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Admin.
ADMINS = (
    ('Web Services', 'jpvelez@gmail.com'),
)
MANAGERS = ADMINS

# site id for the django sites framework
SITE_ID = 1

# internationalization nonsense
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT,'apps','main','static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '&x-iseoz*ul3^2efr%$83(5&571=%2ur%zdep8j^8nj9vwj)pr'

# Where urls.py lives.
ROOT_URLCONF = 'apps.main.urls'

# A template, example.html, is searched for in these template
# directories *after* django searches in the app template
# directories. The order here is important!
TEMPLATE_DIRS = (

    # this is where you should over-ride all project-specific
    # customizations of particular templates
    os.path.join(PROJECT_ROOT, 'apps', 'main', 'templates', ), 

#     # this is where we store (and continue to develop) common
#     # templates that are used across several different django projects
#     os.path.join(PROJECT_ROOT, 'common', 'templates', ), 

#     # this is provided so that it is possible to extend base templates
#     # that are provided by a particular app. For example, the
#     # clientpage app has a base template that we probably want to keep
#     # constant across several different clients.
#     os.path.join(PROJECT_ROOT, 'apps'), 
)

TEMPLATE_CONTEXT_PROCESSORS += (
    
    # add this to get the request object in the django template by
    # default
    'django.core.context_processors.request',

)

# redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# these are all of the django apps that are installed by default. we
# chose to be relatively agressive here --- including more apps does
# not hurt anything
INSTALLED_APPS = (

    # these are provided by django by default
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',    

    # enable the admin and local documentation
    'django.contrib.admin',
    'django.contrib.admindocs',

    # handy django apps for development etc.
    'django.contrib.humanize',
    'django.contrib.webdesign',

)

# add the project apps and the common apps directory on python path so
# that views, models, urls, etc. can do things like 'import
# app.models' without things breaking.
sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))

# set up memcached
CACHE_MIDDLEWARE_SECONDS = 1
CACHE_BACKEND = "memcached://localhost:11211/?timeout=%s"%(
    CACHE_MIDDLEWARE_SECONDS,
)
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# need to add some MIDDLEWARE_CLSSES for working with memcached
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE_CLASSES + (
    'django.middleware.cache.FetchFromCacheMiddleware',
)

# Connect to mysql database.
db = yaml.load(open('database.yml', 'r'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db['name'],
        'USER': db['username'],
        'PASSWORD': db['password'],
        'HOST': '',
        'PORT': '',
    }
}


# for Haml
TEMPLATE_LOADERS = (
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
    ) + TEMPLATE_LOADERS
