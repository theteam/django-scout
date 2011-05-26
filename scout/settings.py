"""
This file is for providing default settings, these can and should
be overridden with your Django project's settings.py.
"""
import logging

from django.conf import settings

# Get logging level and formatting settings.
LOGGING_LEVEL = getattr(settings, 'IPADCATALOGUE_LOGGING_LEVEL', logging.INFO)
LOGGING_FORMAT = getattr(settings, 'IPADCATALOGUE_LOGGING_FORMAT', 
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

DEFAULT_RESPONSE_HANDLERS = ('scout.response_handlers.DummyResponseHandler')

RESPONSE_HANDLERS = getattr(settings, 'SCOUT_RESPONSE_HANDLERS', DEFAULT_RESPONSE_HANDLERS)
