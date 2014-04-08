__author__ = 'gotlium'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def raise_exception(self):
        raise Exception('Hello, World!')

    def handle(self, *args, **options):
        self.raise_exception()
