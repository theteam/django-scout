"""
This file is included as naturaltime is only currently
in the development branch of django (post 1.3, pre 1.4).
naturalday is included so people don't have to add
django.contrib.humanize to their INSTALLED_APPS (but they
may do so).
"""
from datetime import date, datetime, timedelta

from django import template
from django.template import defaultfilters
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.tzinfo import LocalTimezone

register = template.Library()

@register.filter
def naturalday(value, arg=None):
    """
    For date values that are tomorrow, today or yesterday compared to
    present day returns representing string. Otherwise, returns a string
    formatted according to settings.DATE_FORMAT.
    """
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).replace(microsecond=0, second=0, minute=0, hour=0)
    delta = value - today.date()
    if delta.days == 0:
        return _(u'today')
    elif delta.days == 1:
        return _(u'tomorrow')
    elif delta.days == -1:
        return _(u'yesterday')
    return defaultfilters.date(value, arg)

@register.filter
def naturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    try:
        value = datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except AttributeError:
        return value
    except ValueError:
        return value

    if getattr(value, 'tzinfo', None):
        now = datetime.now(LocalTimezone(value))
    else:
        now = datetime.now()
    now = now - timedelta(0, 0, now.microsecond)
    if value < now:
        delta = now - value
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s ago'
            ) % {'delta': defaultfilters.timesince(value)}
        elif delta.seconds == 0:
            return _(u'now')
        elif delta.seconds < 60:
            return ungettext(
                u'a second ago', u'%(count)s seconds ago', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds / 60 < 60:
            count = delta.seconds / 60
            return ungettext(
                u'a minute ago', u'%(count)s minutes ago', count
            ) % {'count': count}
        else:
            count = delta.seconds / 60 / 60
            return ungettext(
                u'an hour ago', u'%(count)s hours ago', count
            ) % {'count': count}
    else:
        delta = value - now
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s from now'
            ) % {'delta': defaultfilters.timeuntil(value)}
        elif delta.seconds == 0:
            return _(u'now')
        elif delta.seconds < 60:
            return ungettext(
                u'a second from now', u'%(count)s seconds from now', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds / 60 < 60:
            count = delta.seconds / 60
            return ungettext(
                u'a minute from now', u'%(count)s minutes from now', count
            ) % {'count': count}
        else:
            count = delta.seconds / 60 / 60
            return ungettext(
                u'an hour from now', u'%(count)s hours from now', count
            ) % {'count': count}
