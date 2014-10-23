# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

import optparse
import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from mmc.models import MMCHost, MMCLog, MMCScript
from mmc.defaults import CLEANUP_IGNORED


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '-l', '--delta', action='store', dest='delta', default=0),
        optparse.make_option(
            '-d', '--date', action='store', dest='date', default=None),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.days_delta = 0

    def _set_delta(self, options):
        self.days_delta = now() - datetime.timedelta(
            days=int(options.get('delta')))

        if options.get('date'):
            dt = datetime.datetime.strptime(options.get('date'), '%Y-%m-%d')
            self.days_delta = (now() - dt)

    def _cleanup_model(self, model):
        model.objects.filter(created__lte=self.days_delta).delete()

    @staticmethod
    def _cleanup_ignored():
        if CLEANUP_IGNORED is True:
            MMCLog.objects.filter(
                script__ignore=True, script__save_on_error=False).delete()

    def _cleanup(self):
        self._cleanup_model(MMCScript)
        self._cleanup_model(MMCHost)
        self._cleanup_model(MMCLog)
        self._cleanup_ignored()

    def handle(self, **options):
        self._set_delta(options)
        self._cleanup()
