"""
Django settings for openshift project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import imp

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
     ON_OPENSHIFT = True

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

default_keys = { 'SECRET_KEY': 'vm4rl5*ymb@2&d_(gc$gb-^twq9w(u69hi--%$5xrh!xk(t%hw' }
use_keys = default_keys

if ON_OPENSHIFT:
     imp.find_module('openshiftlibs')
     import openshiftlibs
     use_keys = openshiftlibs.openshift_secure(default_keys)

SECRET_KEY = use_keys['SECRET_KEY']

if ON_OPENSHIFT:
     #DEBUG = False
     DEBUG = True
else:
     DEBUG = True

TEMPLATE_DEBUG = DEBUG

if DEBUG:
     ALLOWED_HOSTS = []
else:
     ALLOWED_HOSTS = ['*']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# If you want configure the REDISCLOUD
if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
    redis_server = os.environ['REDISCLOUD_URL']
    redis_port = os.environ['REDISCLOUD_PORT']
    redis_password = os.environ['REDISCLOUD_PASSWORD']
    CACHES = {
        'default' : {
            'BACKEND' : 'redis_cache.RedisCache',
            'LOCATION' : '%s:%d'%(redis_server,int(redis_port)),
            'OPTIONS' : {
                'DB':0,
                'PARSER_CLASS' : 'redis.connection.HiredisParser',
                'PASSWORD' : redis_password,
            }
        }
    }
    MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
     os.path.join(BASE_DIR,'templates'),
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if ON_OPENSHIFT:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'db.sqlite3'),
         }
     }
else:
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True 
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#MY_SETTINGS
LOGIN_URL = '/user/login/'
APPEND_SLASH = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #my
    'social.apps.django_app.default',
    'south',
    'forum',
    'userprofile',
    'blog',
    'basesite',

)

#SOCIAL AUTHORIZATION
SOCIAL_AUTH_PIPELINE = (
'social.pipeline.social_auth.social_details',
'social.pipeline.social_auth.social_uid',
'social.pipeline.social_auth.auth_allowed',
'social.pipeline.social_auth.social_user',
'social.pipeline.user.get_username',
'social.pipeline.user.create_user',
'social.pipeline.social_auth.associate_user',
'social.pipeline.social_auth.load_extra_data',
'social.pipeline.user.user_details',
'userprofile.pipeline.user_details',
'userprofile.pipeline.get_user_avatar',
)

LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
ACCESS_TOKEN_METHOD = 'GET'

AUTHENTICATION_BACKENDS = (
  #'social.backends.google.GoogleOAuth2Backend',
  #'social.backends.open_id.OpenIdAuth',
  #'social.backends.google.GoogleOpenId',
  #'social.backends.google.GoogleOAuth2',
#  'social.backends.google.GoogleOAuth',
  #'social.backends.yahoo.YahooOpenId',
  'social.backends.facebook.FacebookOAuth2',
  'social.backends.twitter.TwitterOAuth',
  'social.backends.github.GithubOAuth2',
  'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
)

#twitter
SOCIAL_AUTH_TWITTER_KEY = 'ywIdQZ8GEcVPro2pMdAY7FRvy'
SOCIAL_AUTH_TWITTER_SECRET = 'HBgvGu16JwHn6SYB9HfcLbIagsgwyAii3TH5winvXilwWTPkvq'

#github
SOCIAL_AUTH_GITHUB_KEY = '418f1b0de987958ca56d'
SOCIAL_AUTH_GITHUB_SECRET = '261db37446f05b88da1e5c0a915708491718aacc'

#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '1385525765034186'
SOCIAL_AUTH_FACEBOOK_SECRET = 'ca9e0b0c014909384c3d63336a9ea33e'

SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'twitter', 'facebook', 'github')
