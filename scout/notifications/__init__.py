"""Here we check the settings for the handlers we need to load in
and attach to the post_save signal for when a StatusChange gets saved.
"""
from django.db.models.signals import post_save

from scout.models import StatusChange
from scout.notifications.settings import NOTIFICATION_HANDLERS
from scout.utils import get_module_from_module_string


handler_classes = []

# First we load in all the classes specified in the
# settings (without instantiating them)
for handler_string in NOTIFICATION_HANDLERS:
    handler_classes.append(get_module_from_module_string(handler_string))

# Then we iterate over the classes and connect their as_signal 
# method to the post_save
for handler in handler_classes:
    instance = handler()
    post_save.connect(instance.as_signal, sender=StatusChange, weak=False,
                      dispatch_uid='scout.notifications.handlers.%s' % \
                              handler.__name__)
