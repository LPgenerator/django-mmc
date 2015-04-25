__author__ = 'gotlium'

from time import sleep

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        sleep(300)
        print("OK")
