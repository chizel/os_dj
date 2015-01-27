"""
WSGI config for openshift project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import sys
import os
import django

sys.path.append("PATH")
os.environ['DJANGO_SETTINGS_MODULE'] = "settings" 
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
