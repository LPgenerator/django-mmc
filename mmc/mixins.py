__author__ = 'gotlium'

__all__ = ['BaseCommand', 'NoArgsCommand', 'inject_management']

import traceback
import resource
import socket
import atexit
import time
import sys
import os

from django.core.management.base import NoArgsCommand as NoArgsCommandOrigin
from django.core.management.base import BaseCommand as BaseCommandOrigin
from django.utils.encoding import smart_str
from django.db.utils import DatabaseError

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    now = datetime.now

from mmc.defaults import (
    SENTRY_NOTIFICATION, EMAIL_NOTIFICATION, READ_STDOUT, SUBJECT_LIMIT
)
from mmc.lock import get_lock_instance
from mmc.utils import monkey_mix
from mmc import PY2


def mmc_is_test():
    return sys.argv[1:3] == ['test', 'mmc']


class StdOut(object):
    def __init__(self):
        self.data = []

    def write(self, message):
        self.data.append(message)

        try:
            sys.__stdout__.write(message)
        except Exception as err:
            sys.stderr.write("{0}".format(err))

    def __getattr__(self, method):
        def call_method(*args, **kwargs):
            return getattr(sys.__stdout__, method)(*args, **kwargs)

        return call_method

    def get_stdout(self):
        return self.data


class BaseCommandMixin(object):
    def __init__(self):
        if hasattr(self, '_no_monkey'):
            self._no_monkey.__init__(self)
        else:
            super(BaseCommandMixin, self).__init__()

        if READ_STDOUT is True:
            try:
                __IPYTHON__
            except NameError:
                sys.stdout = StdOut()

        self._mmc_start_date = now()
        self._mmc_start_time = time.time()
        self._mmc_elapsed = None
        self._mmc_success = True
        self._mmc_error_message = None
        self._mmc_traceback = None
        self._mmc_show_traceback = False
        self._mmc_script = self.__module__.split('.')[-1]
        self._mmc_lock = get_lock_instance(self._mmc_script)
        self._mmc_exc_info = None
        self._mmc_hostname = socket.gethostname()
        self._mmc_log_instance = None
        self._mmc_resources = resource.getrusage(resource.RUSAGE_SELF)

    def __mmc_one_copy(self):
        try:
            from mmc.models import MMCScript

            try:
                if MMCScript.get_one_copy(self._mmc_script):
                    self._mmc_lock.check_is_running()
                    self._mmc_lock.lock()
            except MMCScript.DoesNotExist:
                pass
        except Exception as err:
            print("[MMC] {0}".format(err))

    def __mmc_init(self, *args, **options):
        if not mmc_is_test():
            self.__mmc_one_copy()
            atexit.register(self._mmc_at_exit_callback)
            self._mmc_show_traceback = options.get('traceback', False)

    def __mmc_run(self, *args, **options):
        if hasattr(self, '_no_monkey'):
            self._no_monkey.execute(self, *args, **options)
        else:
            super(BaseCommandMixin, self).execute(*args, **options)

    def __mmc_execute(self, *args, **options):
        try:
            self.__mmc_run(*args, **options)
        except Exception as err:
            self._mmc_success = False
            if PY2 is True:
                self._mmc_error_message = err.__unicode__()
            else:
                self._mmc_error_message = err.__str__()
            self._mmc_traceback = traceback.format_exc()
            self._mmc_exc_info = sys.exc_info()
            if not mmc_is_test():
                raise

    def __mmc_done(self):
        if mmc_is_test():
            self._mmc_at_exit_callback()

    def execute(self, *args, **options):
        self.__mmc_init(*args, **options)
        self.__mmc_log_start()
        self.__mmc_execute(*args, **options)
        self.__mmc_done()

    def __mmc_get_sys_argv(self):
        if PY2 is True:
            return ' '.join(map(unicode, sys.argv))
        return ' '.join(map(str, sys.argv))

    def __mmc_log_start(self):
        try:
            from mmc.models import MMCLog

            self._mmc_log_instance = MMCLog.logging(
                start=self._mmc_start_date,
                hostname=self._mmc_hostname,
                script=self._mmc_script,
                elapsed=0.00,
                success=None,
                error_message="",
                traceback="",
                sys_argv=self.__mmc_get_sys_argv(),
                memory=0.00,
                cpu_time=0.00
            )
        except DatabaseError:
            pass
        except Exception as err:
            print("[MMC] Logging broken with message: {0}".format(err))

    def __mmc_store_log(self):
        try:
            from mmc.models import MMCLog

            memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            resources = resource.getrusage(resource.RUSAGE_SELF)

            utime = resources.ru_utime - self._mmc_resources.ru_utime
            stime = resources.ru_stime - self._mmc_resources.ru_stime
            div = 1024.0 if 'linux' in sys.platform else 1048576.0

            MMCLog.logging(
                instance=self._mmc_log_instance,
                start=self._mmc_start_date,
                hostname=self._mmc_hostname,
                script=self._mmc_script,
                elapsed="%0.2f" % (time.time() - self._mmc_start_time),
                success=self._mmc_success,
                error_message=self._mmc_error_message,
                traceback=self._mmc_traceback,
                sys_argv=self.__mmc_get_sys_argv(),
                memory="%0.2f" % (memory / div),
                cpu_time="%0.2f" % (utime + stime),
                stdout_messages=self.__mmc_get_stdout(),
                pid=os.getpid(),
            )
        except Exception as err:
            print("[MMC] Logging broken with message: {0}".format(err))

    def __mmc_get_stdout(self):
        if hasattr(sys.stdout, 'get_stdout'):
            try:
                return u''.join(map(force_unicode, sys.stdout.get_stdout()))
            except:
                return repr(sys.stdout.get_stdout())
        return ''

    def __mmc_get_msg_trace(self):
        traceback_msg = ''
        if hasattr(self._mmc_log_instance, 'pk'):
            traceback_msg += '#%d\n\n' % self._mmc_log_instance.pk
        if self._mmc_traceback:
            traceback_msg += self._mmc_traceback
        return traceback_msg

    def __mmc_send_mail(self):
        if not self._mmc_success and EMAIL_NOTIFICATION:
            from mmc.models import MMCEmail

            MMCEmail.send(
                self._mmc_hostname, self._mmc_script,
                self.__mmc_get_msg_trace()
            )

    def __mmc_send2sentry(self):
        if not self._mmc_success and SENTRY_NOTIFICATION:
            try:
                from raven.contrib.django.raven_compat.models import client

                client.captureException(
                    exc_info=self._mmc_exc_info, extra=dict(os.environ))
            except:
                pass

    def __mmc_print_log(self):
        if not self._mmc_success and not mmc_is_test():
            if self._mmc_show_traceback:
                print(self._mmc_traceback)
            else:
                sys.stderr.write(smart_str(
                    'Error: %s\n' % self.style.ERROR(self._mmc_error_message)
                ))
            sys.exit(1)

    def __mmc_notification(self):
        from mmc.models import MMCEmail, MMCLog

        if not self._mmc_log_instance or mmc_is_test():
            return

        cls = MMCLog.objects.get(pk=self._mmc_log_instance.pk)
        if EMAIL_NOTIFICATION and cls.script.enable_triggers is True:
            script = cls.script
            reason = []
            text = ''

            if script.trigger_cpu and cls.cpu_time > script.trigger_cpu:
                reason.append(('cpu', cls.cpu_time, script.trigger_cpu))
            if script.trigger_memory and cls.memory > script.trigger_memory:
                reason.append(('memory', cls.memory, script.trigger_memory))
            if script.trigger_time and cls.elapsed > script.trigger_time:
                reason.append(('time', cls.elapsed, script.trigger_time))

            if reason:
                for data in reason:
                    text += '%s: %f > %f\n' % data

                MMCEmail.send(
                    self._mmc_hostname, self._mmc_script, text, SUBJECT_LIMIT)

    def _mmc_at_exit_callback(self, *args, **kwargs):
        self.__mmc_store_log()
        self._mmc_lock.unlock()
        self.__mmc_notification()
        self.__mmc_send_mail()
        self.__mmc_send2sentry()
        self.__mmc_print_log()


class BaseCommand(BaseCommandMixin, BaseCommandOrigin):
    pass


class NoArgsCommand(BaseCommandMixin, NoArgsCommandOrigin):
    pass


def inject_management():
    monkey_mix(BaseCommandOrigin, BaseCommandMixin)
