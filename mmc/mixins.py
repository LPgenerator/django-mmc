__author__ = 'gotlium'

__all__ = ['BaseCommand', 'NoArgsCommand', 'inject_management']

import traceback
import resource
import atexit
import time
import sys
import os

try:
    import thread
except ImportError:
    import _thread as thread

from django.core.management.base import NoArgsCommand as NoArgsCommandOrigin
from django.core.management.base import BaseCommand as BaseCommandOrigin
from django.db import connections, connection
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
    SENTRY_NOTIFICATION, EMAIL_NOTIFICATION, READ_STDOUT,
    SUBJECT_LIMIT, REAL_TIME_UPDATE, HOSTNAME
)
from mmc.lock import get_lock_instance
from mmc.utils import monkey_mix
from mmc import PY2


def mmc_is_test():
    return sys.argv[1:3] == ['test', 'mmc']


def stderr(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")


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
        self._mmc_success = None
        self._mmc_error_message = None
        self._mmc_traceback = None
        self._mmc_show_traceback = False
        self._mmc_script = self.__module__.split('.')[-1]
        self._mmc_lock = get_lock_instance(self._mmc_script)
        self._mmc_exc_info = None
        self._mmc_hostname = HOSTNAME
        self._mmc_log_instance = None
        self._mmc_resources = resource.getrusage(resource.RUSAGE_SELF)
        self._mmc_mon_is_run = None
        self._mmc_mon_is_ok = False

    def run_at_subprocess(self, use_subprocess, foo, *args, **kwrags):
        """
        This method for run some function at subprocess.
        Very useful when you have a problem with memory leaks.
        """
        if use_subprocess is False:
            return foo(*args, **kwrags)

        child_pid = os.fork()
        if child_pid == 0:
            foo(*args, **kwrags)
            sys.exit(0)
        return os.waitpid(child_pid, 0)[1] == 0

    def __mmc_run_is_allowed(self):
        try:
            from mmc.models import MMCScript

            try:
                if not MMCScript.run_is_allowed(self._mmc_script):
                    sys.stdout.write("Can't be run. Interval restriction\n")
                    sys.exit(-1)
            except MMCScript.DoesNotExist:
                pass
        except Exception as err:
            stderr("[MMC] {0}".format(err))

    def __mmc_is_enabled(self):
        try:
            from mmc.models import MMCScript

            try:
                if not MMCScript.run_is_enabled(self._mmc_script):
                    sys.stdout.write("Temporarily disabled\n")
                    sys.exit(-1)
            except MMCScript.DoesNotExist:
                pass
        except Exception as err:
            stderr("[MMC] {0}".format(err))

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
            stderr("[MMC] {0}".format(err))

    def __mmc_monitor(self):
        while self._mmc_mon_is_run is True:
            self.__mmc_store_log()
            time.sleep(REAL_TIME_UPDATE)
        self._mmc_mon_is_ok = True

    def __mmc_run_monitor(self):
        if self._mmc_log_instance and self._mmc_log_instance.script.real_time:
            with thread.allocate_lock():
                if self._mmc_mon_is_run is None:
                    self._mmc_mon_is_run = True
                    thread.start_new_thread(self.__mmc_monitor, ())

    def __mmc_stop_monitor(self):
        self._mmc_mon_is_run = False
        if self._mmc_log_instance and self._mmc_log_instance.script.real_time:
            self._mmc_mon_is_run = False
            while self._mmc_mon_is_ok is False:
                time.sleep(1)

    def __mmc_init(self, **options):
        if not mmc_is_test():
            self.__mmc_run_is_allowed()
            self.__mmc_is_enabled()
            self.__mmc_one_copy()
            atexit.register(self._mmc_at_exit_callback)
            self._mmc_show_traceback = options.get('traceback', False)

    def __mmc_run(self, *args, **options):
        if hasattr(self, '_no_monkey'):
            self._no_monkey.execute(self, *args, **options)
        else:
            super(BaseCommandMixin, self).execute(*args, **options)

    def __mmc_enable_queries(self):
        if self._mmc_log_instance:
            if self._mmc_log_instance.script.enable_queries:
                connection.use_debug_cursor = True

    def __mmc_execute(self, *args, **options):
        try:
            self.__mmc_run(*args, **options)
            self._mmc_success = True
        except (Exception, KeyboardInterrupt) as err:
            self._mmc_success = False
            self._mmc_error_message = err
            self._mmc_traceback = traceback.format_exc()
            self._mmc_exc_info = sys.exc_info()
            if not mmc_is_test():
                raise

    def __mmc_done(self):
        if mmc_is_test():
            self._mmc_at_exit_callback()

    def execute(self, *args, **options):
        self.__mmc_init(**options)
        self.__mmc_log_start()
        self.__mmc_run_monitor()
        self.__mmc_enable_queries()
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
                cpu_time=0.00,
                queries=self.__mmc_get_queries(),
            )
        except DatabaseError:
            pass
        except Exception as err:
            stderr("[MMC] Logging broken with message: {0}".format(err))

    def __mmc_get_queries(self, queries=0):
        for db in connections.all():
            queries += len(db.queries)
        return queries

    def __mmc_store_log(self, final=False):
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
                queries=self.__mmc_get_queries(),
                is_fixed=False if self._mmc_success is False else None,
                end=now() if final else self._mmc_log_instance.end
            )
        except Exception as err:
            stderr("[MMC] Logging broken with message: {0}".format(err))

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
        if self._mmc_success is False and EMAIL_NOTIFICATION:
            from mmc.models import MMCEmail

            MMCEmail.send(
                self._mmc_hostname, self._mmc_script,
                self.__mmc_get_msg_trace()
            )

    def __mmc_send2sentry(self):
        if self._mmc_success is False and SENTRY_NOTIFICATION:
            try:
                from raven.contrib.django.raven_compat.models import client

                client.captureException(
                    exc_info=self._mmc_exc_info, extra=dict(os.environ))
            except:
                pass

    def __mmc_print_log(self):
        if self._mmc_success is False and not mmc_is_test():
            if self._mmc_show_traceback:
                print(self._mmc_traceback)
            else:
                stderr(smart_str(self._mmc_error_message))

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
            if script.trigger_queries and cls.queries > script.trigger_queries:
                reason.append(('queries', cls.queries, script.trigger_queries))

            if reason:
                for data in reason:
                    text += '%s: %f > %f\n' % data

                MMCEmail.send(
                    self._mmc_hostname, self._mmc_script, text, SUBJECT_LIMIT)

    def _mmc_at_exit_callback(self, *args, **kwargs):
        self.__mmc_stop_monitor()
        self.__mmc_store_log(final=True)
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
