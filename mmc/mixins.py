__author__ = 'gotlium'

import traceback
import tempfile
import socket
import atexit
import time
import sys
import os

from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    now = datetime.now

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
        self._tempdir = tempfile.gettempdir()
        self._script = sys.argv[1]

    def __mmc_get_lock_file(self):
        return os.path.join(self._tempdir, self._script + '.lock')

    def __mmc_unlock(self):
        if self.__mmc_is_run():
            os.unlink(self.__mmc_get_lock_file())

    def __mmc_lock(self):
        open(self.__mmc_get_lock_file(), 'w').close()

    def __mmc_is_run(self):
        return os.path.exists(self.__mmc_get_lock_file())

    def __mmc_check_is_running(self):
        if self.__mmc_is_run():
            sys.stdout.write('Already running\n')
            sys.exit(-1)

    def __mmc_one_copy(self):
        try:
            from models import MMCScript

            if MMCScript.get_one_copy(self._script):
                self.__mmc_check_is_running()
                self.__mmc_lock()
        except Exception, msg:
            print '[MMC]', msg.__str__()

    def execute(self, *args, **options):
        self.__mmc_one_copy()
        atexit.register(self._mmc_atexit_callback)
        self._show_traceback = options.get('traceback', False)

        try:
            self._no_monkey.execute(self, *args, **options)
        except Exception, ex:
            self._success = False
            self._error_message = ex.__str__()
            self._traceback = traceback.format_exc()

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
            print '[MMC] Logging broken with message:', msg.__str__()

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
        self.__mmc_print_log()
        self.__mmc_unlock()


def inject_management():
    monkey_mix(BaseCommand, BaseCommandMixin)
