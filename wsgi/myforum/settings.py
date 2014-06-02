"""
Django settings for myforum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

LOGIN_URL = '/forum/login/'
APPEND_SLASH = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z$u-)@51y$bsx(pqi*^o0m)u-+djrv@%%3w_9yripfhs)$(qlb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'forum',
    'userprofile',
    'blog',
    'basesite',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myforum.urls'

WSGI_APPLICATION = 'myforum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        'USER': '',
        #'PASSWORD': '',
        #'HOST': '',
#        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/d/git/python/myforum/static/'
#STATICFILES_DIRS = (
        #os.path.join(BASE_DIR, 'static'),
        ##'/var/www/static/',
#        )

# OAUTH

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
ACCESS_TOKEN_METHOD = 'GET'

AUTHENTICATION_BACKENDS = (
  #'social.backends.google.GoogleOAuth2Backend',
  'social.backends.github.GithubOAuth2',
  'social.backends.open_id.OpenIdAuth',
  'social.backends.google.GoogleOpenId',
  'social.backends.google.GoogleOAuth2',
  'social.backends.google.GoogleOAuth',
  'social.backends.twitter.TwitterOAuth',
  'social.backends.yahoo.YahooOpenId',
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

SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'twitter', 'facebook', 'github')

