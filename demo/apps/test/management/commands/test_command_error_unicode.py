# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

from django.core.management.base import BaseCommand
import mmc


class Command(BaseCommand):
    def raise_exception(self):
        if mmc.PY2 is True:
            raise Exception(u'Привет, мир!')
        raise Exception('Привет, мир!')

    def handle(self, *args, **options):
        self.raise_exception()
