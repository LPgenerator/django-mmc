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
except:
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

    def execute(self, *args, **options):
        atexit.register(self._save_results)
        self._show_traceback = options.get('traceback', False)

        try:
            self._no_monkey.execute(self, *args, **options)
        except Exception, ex:
            self._success = False
            self._error_message = ex.__str__()
            self._traceback = traceback.format_exc()

    def _save_results(self, *args, **kwargs):
        try:
            from mmc.models import MMCLog

            MMCLog.logging(
                start=self._start_date,
                hostname=socket.gethostname(),
                script=sys.argv[1],
                elapsed="%0.2f" % (time.time() - self._start_time),
                success=self._success,
                error_message=self._error_message,
                traceback=self._traceback,
                sys_argv=' '.join(map(unicode, sys.argv))
            )
        except Exception, msg:
            print 'Logging broken with message:', msg

        if not self._success:
            if self._show_traceback:
                print self._traceback
            else:
                sys.stderr.write(smart_str(
                    'Error: %s\n' % self.style.ERROR(self._error_message)
                ))
            sys.exit(1)


def inject_management():
    monkey_mix(BaseCommand, BaseCommandMixin)
