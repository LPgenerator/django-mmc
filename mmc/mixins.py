__author__ = 'gotlium'

from . import BaseCommand

from django.core import management


def inject_management():
    # for backwards compatibility
    management.base.BaseCommand = BaseCommand
    management.BaseCommand = BaseCommand
