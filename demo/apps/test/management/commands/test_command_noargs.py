__author__ = 'gotlium'

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, *args, **options):
        print("OK")
