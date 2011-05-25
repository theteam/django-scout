"""
This file is for providing default settings, these can and should
be overridden with your Django project's settings.py.
"""
from django.conf import settings

DEFAULT_RESPONSE_HANDLERS = ()

RESPONSE_HANDLERS = getattr(settings, 'SCOUT_RESPONSE_HANDLERS', DEFAULT_RESPONSE_HANDLERS)
