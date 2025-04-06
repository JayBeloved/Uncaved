"""
ASGI config for uncaved project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncaved.settings.local')
if os.getenv('ENV') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncaved.settings.production')


application = get_asgi_application()
