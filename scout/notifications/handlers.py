from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, string_concat

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
    """This is the base class for the email handlers and
    as such should not be used directly without subclassing.
    """

    def _get_emails(self):
        """Should return an iterative of email addresses.
        """
        raise NotImplementedError

    def _get_templates(self):
        """Returns a two element tuple of template paths.
        The first one being for errors, and the second one
        for recovery use.
        """
        return ('scout/notifications/email/expected.txt',
                'scout/notifications/email/unexpected.txt')

    def send_emails(self, subject, rendered_template, emails): 
        """Should, given a list of emails and a rendered
        template, dispatch an email to those that need it.
        """
        send_mail(subject, rendered_template, FROM_EMAIL, emails)

    def as_signal(self, sender, instance, created, using, **kwargs):
        """The signal connector.
        """
        if created:
            subject = u"%s " % settings.EMAIL_SUBJECT_PREFIX
            context = {'log': instance}
            error_template, recovery_template = self._get_templates()
            if instance.is_error():
                template = error_template
                subject = string_concat(subject, _("PROBLEM: "))
            else:
                template = recovery_template 
                subject = string_concat(subject, _("RECOVERED: "))
            subject += u"%s %s" % (instance.test.project.client,
                                  instance.test.project)
            rendered = render_to_string(template, context)
            self.send_emails(subject, rendered, self._get_emails())


class AdminEmailNotificationHandler(EmailNotificationHandler):
    """An email-based notification handler which simply
    emails all the ADMINS located in the settings file.
    """

    def _get_emails(self):
        return [x[1] for x in settings.ADMINS]


class ManagersEmailNotificationHandler(EmailNotificationHandler):
    """An email-based notification handler which simply
    emails all the MANAGERS located in the settings file.
    """

    def _get_emails(self):
        return [x[1] for x in settings.MANAGERS]


class ProfileEmailNotificationHandler(EmailNotificationHandler):
    """An email-based notification handler which ties in with
    the user profile system to support more of a subscription
    based notifying system.
    """

    def __init__(self, *args, **kwargs):
        #TODO: Implement this; will require extra for handling
        # user subscriptions to certain projects (I wouldn't
        # handle subs on a per test basis, that seems too deep)
        raise NotImplementedError

    def _get_emails(self):
        raise NotImplementedError

    def as_signal(self, sender, instance, created, using, **kwargs):
        pass
