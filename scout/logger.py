import logging
import sys

from scout.settings import LOGGING_LEVEL, LOGGING_FORMAT

log = logging.getLogger('django-scout')

formatter = logging.Formatter(LOGGING_FORMAT)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)

log.addHandler(stream)
log.setLevel(LOGGING_LEVEL)

__all__ = ['log']
