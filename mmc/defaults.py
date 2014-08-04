# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


SUBJECT = get_settings('MMC_SUBJECT', '[MMC] Errors')

REDIS_CONFIG = get_settings('MMC_REDIS_CONFIG', {
    'host': 'localhost', 'port': 6379,
    'db': 0, 'password': None
})
MEMCACHED_CONFIG = get_settings('MMC_MEMCACHED_CONFIG', {
    'servers': ['127.0.0.1:11211'], 'debug': 0
})
LOCK_TYPE = get_settings('MMC_LOCK_TYPE', 'FileLock')
