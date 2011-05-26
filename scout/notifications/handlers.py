from scout.logger import log
from scout.models import StatusChange

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
            if instance.result == StatusChange.EXPECTED:
                log.info("[EXPECTED] Recovered from an unexpected " \
                         "response last run. <%s>" % instance.test.url)
            elif instance.result == StatusChange.UNEXPECTED:
                log.info("[UNEXPECTED] Exp: %s, rec: %s. <%s>" % (
                                                    instance.expected_status,
                                                    instance.returned_status,
                                                    instance.test.url))


class EmailNotificationHandler(BaseNotificationHandler):
    """A notification handler which uses email as its 
    notification medium. Will send to the email address
    on file for the user.
    """

    def as_signal(self, sender, instance, created, using, **kwargs):
        pass
