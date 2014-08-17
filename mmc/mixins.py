__author__ = 'gotlium'

import traceback
import socket
import atexit
import time
import sys

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    now = datetime.now

from lock import get_lock_instance
from utils import monkey_mix


class BaseCommandMixin(object):
    def __init__(self):
        self._no_monkey.__init__(self)

        self._start_date = now()
        self._start_time = time.time()
        self._elapsed = None
        self._success = True
        self._error_message = None
        self._traceback = None
        self._show_traceback = False
        self._script = self.__module__.split('.')[-1]
        self._lock = get_lock_instance(self._script)

    def __mmc_one_copy(self):
        try:
            from models import MMCScript

            try:
                if MMCScript.get_one_copy(self._script):
                    self._lock.check_is_running()
                    self._lock.lock()
            except MMCScript.DoesNotExist:
                pass
        except Exception, msg:
            print '[MMC]', msg.__unicode__()

    def execute(self, *args, **options):
        self.__mmc_one_copy()
        atexit.register(self._mmc_atexit_callback)
        self._show_traceback = options.get('traceback', False)

        try:
            self._no_monkey.execute(self, *args, **options)
        except Exception as ex:
            self._success = False
            self._error_message = ex.__unicode__()
            self._traceback = traceback.format_exc()
            raise

    def __mmc_store_log(self):
        try:
            from mmc.models import MMCLog

            MMCLog.logging(
                start=self._start_date,
                hostname=socket.gethostname(),
                script=self._script,
                elapsed="%0.2f" % (time.time() - self._start_time),
                success=self._success,
                error_message=self._error_message,
                traceback=self._traceback,
                sys_argv=' '.join(map(unicode, sys.argv))
            )
        except Exception, msg:
            print '[MMC] Logging broken with message:', msg.__unicode__()

    def __mmc_send_mail(self):
        if not self._success:
            from mmc.models import MMCEmail

            MMCEmail.send(self._traceback)

    def __mmc_print_log(self):
        if not self._success:
            if self._show_traceback:
                print self._traceback
            else:
                sys.stderr.write(smart_str(
                    'Error: %s\n' % self.style.ERROR(self._error_message)
                ))
            sys.exit(1)

    def _mmc_atexit_callback(self, *args, **kwargs):
        self.__mmc_store_log()
        self.__mmc_send_mail()
        self._lock.unlock()
        self.__mmc_print_log()


def inject_management():
    monkey_mix(BaseCommand, BaseCommandMixin)
