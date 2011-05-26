from urllib2 import URLError

import requests
from scout.logger import log
from scout.models import StatusTest, StatusChange


class PingRunner(object):
    """
    The core of the live site monitor, this class runs
    the request tests and deals with them appropriately.
    """

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

    def run_tests(self):
        """
        The actual runner method, runs the test and reports back
        True if it ran succesfully.
        """
        tests = self.get_tests()
        for test in tests:
            self.run_single_test(test)

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
            #TODO LOG
            log.info('URL failed. %s' % e)
            return
        #TODO run handlers
        if self._is_loggable(self, test, response):
            self._log()


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
                last_log = StatusChange.objects.filter(test=test).order_by('-date_added')[0]
            except IndexError:
                # No status change logs exist for this test, either first run or 
                # never had a failure so it is not necessary to log.
                return False
            else:
                if last_log.result == StatusChange.UNEXPECTED:
                    # The last log found was an error, as we're not getting the
                    # expected result back, we need to log this success.
                    return True
                else:
                    # The last log found was a success, therefore we do not need
                    # to log further requests (as uptime is assumed).
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
        if response:
            data['returned_status'] = response.status_code
            data['result'] = StatusChange.UNEXPECTED \
                                if test.expected_status != response.status_code \
                                else StatusChange.EXPECTED
        else:
            data['result'] = StatusChange.UNEXPECTED
        log = StatusChange.objects.create(**data)
        return log
