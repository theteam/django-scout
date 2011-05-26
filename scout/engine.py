from urllib2 import URLError

import requests
from scout.logger import log
from scout.models import StatusTest, StatusChange
from scout.settings import RESPONSE_HANDLERS
from scout.utils import get_module_from_module_string


class PingRunner(object):
    """
    The core of the live site monitor, this class runs
    the request tests and deals with them appropriately.
    """

    def __init__(self, response_handlers=False, *args, **kwargs):
        """
        Initialise the ping runner.
        * response_handlers = an iterative of module strings to load the 
                              response handlers, if none are provided then 
                              the one found via the settings are used.
        """
        if response_handlers:
            self.response_handlers = self._setup_response_handlers(
                                        response_handlers)
        else:
            self.response_handlers = self._setup_response_handlers(
                                        RESPONSE_HANDLERS)

    def _setup_response_handlers(self, response_handlers):
        """
        Returns a list of classes as loaded from the list 
        of dot-seperated module strings passed in.
        """
        handlers = []
        for handler_string in response_handlers:
            handlers.append(get_module_from_module_string(handler_string))
        return handlers

    def get_tests(self):
        """
        Returns a queryset of StatusTest objects which
        will are ready to be tested.
        """
        # Gets all active tests where the project and client
        # are also set to active.
        tests = StatusTest.active.filter(project__is_active=True, 
                                         project__client__is_active=True)
        return tests

    def run_tests(self, tests=False):
        """
        The actual runner method, runs the tests and reports back
        True if it ran succesfully. A queryset of StatusTests can be
        provided for overrideability but the default is to use those
        provided by self.get_tests()
        """
        if not tests:
            tests = self.get_tests()
        for test in tests:
            self.run_single_test(test)
        return

    def run_single_test(self, test):
        """
        Given a StatusTest object, runs the test.
        """
        log.info('Testing URL: %s' % test.url)
        try:
            response = requests.get(test.url)
        except URLError, e:
            # This is a hard error without even an HTTP response
            # and therefore should always be logged.
            log.info('URL failed to provide a response. %s' % e)
            self._log(test, response=False)
            return
        self._run_response_handlers(test, response)
        if self._is_loggable(test, response):
            self._log(test, response)
        return

    def _run_response_handlers(self, test, response):
        """
        Runs all the loaded response handlers against the
        response, this is for plugin-like functionality.
        """
        for handler in self.response_handlers:
            instance = handler(test, response)
            instance.handle_response()
        return

    def _is_loggable(self, test, response):
        """
        Returns True if the rest result should be logged, False otherwise.
        There are two scenarios where we need to log:
            1) If the response status code does not match our expected return.
            2) If the response status code does match our expected returns BUT
               the last time the Pinger ran it recorded a failure.
        """
        if response.status_code != test.expected_status:
            # This is a hard failure, we need to log this
            # to keep track of down time.
            return True
        else:
            try:
                last_log = StatusChange.objects.filter(test=test)\
                           .order_by('-date_added')[0]
            except IndexError:
                # No status change logs exist for this test, either first run 
                # or never had a failure so it is not necessary to log.
                return False
            else:
                if last_log.result == StatusChange.UNEXPECTED:
                    # The last log found was an error, as we're not getting the
                    # expected result back, we need to log this success.
                    return True
                else:
                    # The last log found was a success, therefore we do not 
                    # need to log further requests (as uptime is assumed).
                    return False


    def _log(self, test, response=False):
        """
        Logs a response status change, if no response is provided
        then the presumption is that no response was returned and
        therefore we log as an unexpected event. Returns the created
        log object.
        """
        data = {'test': test,
                'expected_status': test.expected_status}
        # Annoyingly a non success status code will cause the response
        # to evaluate to False so I can't simply test if we have
        # a response by going 'if response'.
        if hasattr(response, 'status_code'):
            data['returned_status'] = response.status_code
            data['result'] = StatusChange.UNEXPECTED if \
                                test.expected_status != response.status_code \
                                else StatusChange.EXPECTED
        else:
            print "logging"
            data['result'] = StatusChange.UNEXPECTED
        log = StatusChange.objects.create(**data)
        return log
