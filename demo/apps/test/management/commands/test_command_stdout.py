# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

import pprint

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Запросы:")
        pprint.pprint(connections['default'].queries, indent=4)
        raise Exception(u"Ошибочка")
