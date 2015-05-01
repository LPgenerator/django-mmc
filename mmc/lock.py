__author__ = 'gotlium'

import tempfile
import datetime
import random
import time
import sys
import os

from mmc import defaults


class AbstractLock(object):
    def __init__(self, script):
        self._script = script
        self._lock_time = self.get_lock_time()
        self._tempdir = tempfile.gettempdir()

    def get_lock_time(self):
        try:
            from mmc.models import MMCLog

            return MMCLog.get_lock_time(self._script)
        except:
            return defaults.DEFAULT_LOCK_TIME

    def get_lock_file(self):
        return os.path.join(self._tempdir, self._script + '.lock')

    def unlock(self):
        raise NotImplementedError

    def lock(self):
        raise NotImplementedError

    def is_run(self):
        raise NotImplementedError

    def check_is_running(self):
        if self.is_run():
            sys.stdout.write('Already running\n')
            sys.exit(-1)

    @staticmethod
    def random_wait():
        random.seed()
        time.sleep(random.choice([random.uniform(0, 3) for i in range(10)]))


class FileLock(AbstractLock):
    def unlock(self):
        if self.is_run():
            os.unlink(self.get_lock_file())

    def lock(self):
        open(self.get_lock_file(), 'w').close()

    def _cleanup_lock(self):
        if os.path.exists(self.get_lock_file()):
            created = datetime.datetime.fromtimestamp(
                os.path.getctime(self.get_lock_file()))
            seconds = (datetime.datetime.now() - created).seconds
            if seconds > self._lock_time:
                os.unlink(self.get_lock_file())

    def is_run(self):
        self._cleanup_lock()
        return os.path.exists(self.get_lock_file())


class RedisLock(AbstractLock):
    def __init__(self, script):
        from redis import StrictRedis

        self._cli = StrictRedis(**defaults.REDIS_CONFIG)
        super(RedisLock, self).__init__(script)
        self.random_wait()

    def unlock(self):
        if self.is_run():
            self._cli.delete(self.get_lock_file())

    def lock(self):
        return self._cli.set(self.get_lock_file(), '1', self._lock_time)

    def is_run(self):
        return self._cli.get(self.get_lock_file())


class MemcacheLock(RedisLock):
    def __init__(self, script):
        try:
            from memcache import Client
        except ImportError:
            from pylibmc import Client

        super(MemcacheLock, self).__init__(script)
        self._cli = Client(**defaults.MEMCACHED_CONFIG)
        self.random_wait()


def get_lock_instance(script):
    return globals().get(defaults.LOCK_TYPE)(script)
