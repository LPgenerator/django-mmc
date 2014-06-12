# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


SUBJECT = get_settings('MMC_SUBJECT', '[MMC] Errors')
