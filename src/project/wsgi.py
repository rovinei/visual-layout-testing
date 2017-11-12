"""
WSGI config for webAutomateTesting project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import signal
import time
import traceback

from django.core.wsgi import get_wsgi_application
sys.path.append('/var/www/pu-ai-test.com')
os.environ["DJANGO_SETTINGS_MODULE"] = "src.project.settings.settings"

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
