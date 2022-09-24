"""
WSGI config for TM30_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from django.core.wsgi import get_wsgi_application

configuration = os.getenv('ENVIRONMENT')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'TM30_project.settings.{configuration}')

application = get_wsgi_application()