# -*- encoding: utf-8 -*-

__author__ = 'gotlium'

import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from mmc.models import MMCLog, MMCEmail


class Command(BaseCommand):
    @staticmethod
    def check_pid(pid, proc_name):
        try:
            import psutil

            if psutil.pid_exists(pid):
                process = psutil.Process(pid)
                if proc_name in process.cmdline():
                    return True
        except ImportError:
            pass

    def handle(self, **options):
        day_ago = (now() - datetime.timedelta(days=1))
        two_day_ago = (day_ago - datetime.timedelta(days=1))
        log_list = MMCLog.objects.filter(
            success__isnull=True, was_notified=False,
            created__range=[two_day_ago, day_ago])

        for log in log_list:
            if self.check_pid(log.pid, log.script.name):
                continue
            MMCEmail.send(
                log.hostname.name, log.script.name,
                'Maybe script "%s" was killed by OS kernel.' % log.script.name)
            log.was_notified = True
            log.save()
