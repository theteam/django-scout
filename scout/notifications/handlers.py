from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from scout.logger import log
from scout.notifications.settings import FROM_EMAIL

class BaseNotificationHandler(object):
    """The base notication handler response, all new handlers 
    should subclass this and extend/override from there.
    """

    def as_signal(self, sender, instance, created, using, **kwargs):
        """This is the method which gets connected to the 
        StatusChange post_save signal.
        """
        raise NotImplementedError


class LoggingNotificationHandler(BaseNotificationHandler):
    """A notificaion handler which uses the Python logging
    module to detail success and failure. This can be picked
    up in the Django settings.py (1.3+) and redirected to 
    something like Sentry for example.
    """

    def as_signal(self, sender, instance, created, using, **kwargs):
        if created:
            if instance.is_error():
                log.info("[UNEXPECTED] Exp: %s, rec: %s. <%s>" % (
                                                    instance.expected_status,
                                                    instance.returned_status,
                                                    instance.test.url))
            else:
                log.info("[EXPECTED] Recovered from an unexpected " \
                         "response last run. <%s>" % instance.test.url)


class EmailNotificationHandler(BaseNotificationHandler):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Do not use this class directly.")

    def _get_emails(self):
        """Should return an iterative of email addresses.
        """
        raise NotImplementedError

    def send_emails(self, subject, rendered_template, emails): 
        """Should, given a list of emails and a rendered
        template, dispatch an email to those that need it.
        """
        send_mail(subject, rendered_template, FROM_EMAIL, emails)


class AdminEmailNotificationHandler(BaseNotificationHandler):
    """ An email-based notification handler which simply
    emails all the Admins located in the settings file.
    """

    def as_signal(self, sender, instance, created, using, **kwargs):
        if created:
            subject = "%s " % settings.EMAIL_SUBJECT_PREFIX
            context = {'log': instance}
            if instance.is_error():
                template = 'scout/notifications/email/admin_expected.txt'
                subject += "ERROR: "
            else:
                template = 'scout/notifications/email/admin_unexpected.txt'
                subject += "RECOVERED: "
            subject += "%s %s" % (instance.project.client,
                                  instance.project)
            rendered = render_to_string(template, context)
            self.send_emails(subject, rendered, self.get_emails())

    def _get_emails(self):
        return [x[1] for x in settings.ADMINS]


class ProfileEmailNotificationHandler(BaseNotificationHandler):
    """An email-based notification handler which ties in with
    the user profile system to support more of a subscription
    based notifying system.
    """

    def __init__(self, *args, **kwargs):
        #TODO: Implement this; will require extra for handling
        # user subscriptions to certain projects (I wouldn't
        # handle subs on a per test basis, that seems too deep)
        raise NotImplementedError

    def as_signal(self, sender, instance, created, using, **kwargs):
        pass
