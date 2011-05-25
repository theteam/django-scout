from optparse import make_option

from django.core.management.base import BaseCommand
from lockfile import FileLock, AlreadyLocked, LockTimeout

from scout.engine import PingRunner
from scout.logger import log

LOCK_WAIT_TIMEOUT = -1

class Command(BaseCommand):
    """
    A management command to run the pinger.
    """

    help = '#TODO'

    option_list = BaseCommand.option_list + (
    )

    def handle(self, *args, **options):
        # Check the lock is free.
        lock = FileLock("django_scout_run_pinger")
        log.info("Acquiring file lock..")
        try:
            lock.acquire(LOCK_WAIT_TIMEOUT)
        except AlreadyLocked:
            log.warn("Lock already in place. Quitting.")
            return
        except LockTimeout:
            log.warn("Waiting for the lock to time out. Quitting.")
            return
        log.info("Lock acquired.")

        try:
            log.info("Starting the pinger..")
            handler = PingRunner()
            handler.run_tests()
        finally:
            lock.release()
            log.info("Released lock.")
