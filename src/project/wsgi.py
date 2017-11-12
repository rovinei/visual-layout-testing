"""
WSGI config for webAutomateTesting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
# sys.path.append('/var/www/pu-ai-test.com')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

application = get_wsgi_application()
