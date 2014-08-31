__author__ = 'gotlium'

import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        os._exit(-1)
