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
        print tests
