import datetime
from urllib2 import URLError

import requests
from scout.logger import log
from scout.models import StatusTest, StatusChange
from scout.settings import RESPONSE_HANDLERS
from scout.utils import get_module_from_module_string



class PingRunner(object):
    """The core of the live site monitor, this class runs
    the request tests and deals with them appropriately.
    """

    def __init__(self, response_handlers=False, *args, **kwargs):
        """Initialise the ping runner.
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
        """Returns a list of classes as loaded from the list 
        of dot-seperated module strings passed in.
        """
        handlers = []
        for handler_string in response_handlers:
            handlers.append(get_module_from_module_string(handler_string))
        return handlers

    def get_tests(self):
        """Returns a queryset of StatusTest objects which
        will are ready to be tested.
        """
        # Gets all active tests where the project and client
        # are also set to active.
        return StatusTest.active.all()

    def run_tests(self, tests=False):
        """The actual runner method, runs the tests and reports back
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
        """Given a StatusTest object, runs the test.
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
        test_log = None
        if self._is_loggable(test, response):
            # Log the result and then update the
            # 'cached' project status based on the log.
            test_log = self._log(test, response)
        self._update_project_status(test, test_log)
        return

    def _run_response_handlers(self, test, response):
        """Runs all the loaded response handlers against the
        response, this is for plugin-like functionality.
        """
        for handler in self.response_handlers:
            instance = handler(test, response)
            instance.handle_response()
        return

    def _is_loggable(self, test, response):
        """Returns True if the rest result should be logged, False otherwise.
        There are two scenarios where we need to log:
            1) If the response status code does not match our expected return
               and this is first occurance of this (since last success).
            2) If the response status code does match our expected returns BUT
               the last time the Pinger ran it recorded a failure.
        Therefore we always need to start by getting the last log.
        """
        try:
            # We should only trust recent logs, thus we
            # only get those from the last hour.
            one_hour = datetime.timedelta(hours=1)
            one_hour_ago = datetime.datetime.now() - one_hour
            last_log = StatusChange.objects.filter(
                                              test=test,
                                              date_added__gte=one_hour_ago
                                            ).order_by('-date_added')[0]
        except IndexError:
            last_log = None
        if response.status_code != test.expected_status:
            # Unexpected response.
            if last_log and not last_log.is_error():
                # RE: 1) Was OK, now not OK. Log.
                return True
            elif last_log is None:
                # RE: 1) No previous log, as this is an
                # error we need to log the first occurance.
                return True
            return False
        else:
            # Expected response.
            if last_log and last_log.is_error():
                # 2) Was not OK, now is OK. Log.
                return True
            return False

    def _log(self, test, response=False):
        """Logs a response status change, if no response is provided
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
            data['result'] = StatusChange.UNEXPECTED
        log = StatusChange.objects.create(**data)
        return log

    def _update_project_status(self, test, log=None):
        """Updates the date_updated timestamp on the project
        so we know when it was last tested and stores a 
        denormalized field on the project showing the current 
        status, this method updates that field based on the 
        logging occurring and whether it was an 
        EXPECTED/UNEXPECTED result.
        """
        project = test.project
        project.date_updated = datetime.datetime.now()
        if not log is None:
            if log.is_error():
                project.working = False
            else:
                project.working = True
        project.save()
        return
