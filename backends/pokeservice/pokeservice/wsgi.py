"""
WSGI config for pokeservice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from .otel import instrument_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokeservice.settings")

application = get_wsgi_application()

application = instrument_application(
    application=application,
    service_name=settings.SERVICE_NAME,
    grpc_receiver_endpoint=settings.GRPC_RECEIVER_ENDPOINT,
)



