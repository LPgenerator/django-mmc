__author__ = 'gotlium'

import time
try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from import django.core.management import BaseCommand as NoArgsCommand



class Command(NoArgsCommand):
    def handle_noargs(self, *args, **options):
        time.sleep(4)
        print("OK.")
