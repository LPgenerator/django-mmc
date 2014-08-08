__author__ = 'gotlium'

import tempfile
import random
import time
import sys
import os

import defaults


class AbstractLock(object):
    def __init__(self, script):
        self._script = script
        self._tempdir = tempfile.gettempdir()

    def get_lock_file(self):
        return os.path.join(self._tempdir, self._script + '.lock')

    def unlock(self):
        raise NotImplemented

    def lock(self):
        raise NotImplemented

    def is_run(self):
        raise NotImplemented

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

    def is_run(self):
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
        return self._cli.set(self.get_lock_file(), '1')

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
