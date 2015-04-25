__author__ = 'gotlium'

import time
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, *args, **options):
        time.sleep(4)
        raise Exception("Error ...")
