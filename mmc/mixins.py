__author__ = 'gotlium'

__all__ = ['BaseCommand', 'NoArgsCommand', 'inject_management']

import traceback
import socket
import atexit
import time
import sys

from django.core.management.base import NoArgsCommand as NoArgsCommandOrigin
from django.core.management.base import BaseCommand as BaseCommandOrigin
from django.utils.encoding import smart_str

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    now = datetime.now

from .lock import get_lock_instance
from .utils import monkey_mix


class BaseCommandMixin(object):
    def __init__(self):
        if hasattr(self, '_no_monkey'):
            self._no_monkey.__init__(self)
        else:
            super(BaseCommandMixin, self).__init__()

        self._mmc_start_date = now()
        self._mmc_start_time = time.time()
        self._mmc_elapsed = None
        self._mmc_success = True
        self._mmc_error_message = None
        self._mmc_traceback = None
        self._mmc_show_traceback = False
        self._mmc_script = self.__module__.split('.')[-1]
        self._mmc_lock = get_lock_instance(self._mmc_script)

    def __mmc_one_copy(self):
        try:
            from models import MMCScript

            try:
                if MMCScript.get_one_copy(self._mmc_script):
                    self._mmc_lock.check_is_running()
                    self._mmc_lock.lock()
            except MMCScript.DoesNotExist:
                pass
        except Exception, msg:
            print '[MMC]', msg.__unicode__()

    def execute(self, *args, **options):
        self.__mmc_one_copy()
        atexit.register(self._mmc_atexit_callback)
        self._mmc_show_traceback = options.get('traceback', False)

        try:
            if hasattr(self, '_no_monkey'):
                self._no_monkey.execute(self, *args, **options)
            else:
                super(BaseCommandMixin, self).execute(*args, **options)
        except Exception as ex:
            self._mmc_success = False
            self._mmc_error_message = ex.__unicode__()
            self._mmc_traceback = traceback.format_exc()
            raise

    def __mmc_store_log(self):
        try:
            from mmc.models import MMCLog

            MMCLog.logging(
                start=self._mmc_start_date,
                hostname=socket.gethostname(),
                script=self._mmc_script,
                elapsed="%0.2f" % (time.time() - self._mmc_start_time),
                success=self._mmc_success,
                error_message=self._mmc_error_message,
                traceback=self._mmc_traceback,
                sys_argv=' '.join(map(unicode, sys.argv))
            )
        except Exception, msg:
            print '[MMC] Logging broken with message:', msg.__unicode__()

    def __mmc_send_mail(self):
        if not self._mmc_success:
            from mmc.models import MMCEmail

            MMCEmail.send(self._mmc_traceback)

    def __mmc_print_log(self):
        if not self._mmc_success:
            if self._mmc_show_traceback:
                print self._mmc_traceback
            else:
                sys.stderr.write(smart_str(
                    'Error: %s\n' % self.style.ERROR(self._mmc_error_message)
                ))
            sys.exit(1)

    def _mmc_atexit_callback(self, *args, **kwargs):
        self.__mmc_store_log()
        self.__mmc_send_mail()
        self._mmc_lock.unlock()
        self.__mmc_print_log()


class BaseCommand(BaseCommandMixin, BaseCommandOrigin):
    pass


class NoArgsCommand(BaseCommandMixin, NoArgsCommandOrigin):
    pass


def inject_management():
    monkey_mix(BaseCommandOrigin, BaseCommandMixin)
