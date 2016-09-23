__author__ = 'gotlium'

import time
try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, *args, **options):
        time.sleep(4)
        raise Exception("Error ...")
