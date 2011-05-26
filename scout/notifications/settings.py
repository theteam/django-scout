"""
This file is for providing default settings, these can and should
be overridden with your Django project's settings.py.
"""
from django.conf import settings

DEFAULT_NOTIFICATION_HANDLERS = (
    'scout.notifications.handlers.LoggingNotificationHandler',
    'scout.notifications.handlers.EmailNotificationHandler',
)

NOTIFICATION_HANDLERS = getattr(settings, 'SCOUT_NOTIFICATION_HANDLERS', 
                                DEFAULT_NOTIFICATION_HANDLERS)
