__author__ = 'gotlium'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    @staticmethod
    def ping(address):
        import os

        os.system('ping -c 4 %s' % address)

    def handle(self, *args, **options):
        use_subprocess = True
        self.run_at_subprocess(use_subprocess, self.ping, '8.8.8.8')
        print("Done")
