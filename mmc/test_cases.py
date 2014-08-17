# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase
from django.core import mail

from mmc.models import MMCScript, MMCLog, MMCHost, MMCEmail
from mmc.defaults import SUBJECT


class MMCTestCase(TestCase):
    def setUp(self):
        MMCEmail.objects.create(email='root@local.host')

    def __test_command(self, command, success):
        call_command(command)

        script = MMCScript.objects.filter(name=command)
        host = MMCHost.objects.all()[0]
        log = MMCLog.objects.filter(script=script, hostname=host)

        self.assertTrue(script.exists())
        self.assertTrue(log.exists())
        self.assertEquals(log.count(), 1)
        self.assertEquals(log[0].success, success)

    def __test_command_ignore(self, command):
        script = MMCScript.objects.create(
            name=command, ignore=True, save_on_error=False)

        call_command(command)

        log = MMCLog.objects.filter(script=script)
        self.assertFalse(log.exists())

    def __check_email(self):
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, SUBJECT)

    # store log
    def test_a_test_command(self):
        self.__test_command('test_command', True)

    def test_b_test_command_noargs(self):
        self.__test_command('test_command_noargs', True)

    def test_c_test_command_error(self):
        self.__test_command('test_command_error', False)
        self.__check_email()

    # ignore log
    def test_a_test_command_ignore(self):
        self.__test_command_ignore('test_command')

    def test_b_test_command_noargs_ignore(self):
        self.__test_command_ignore('test_command_noargs')

    def test_c_test_command_error_ignore(self):
        self.__test_command_ignore('test_command_error')

    # store into log for ignored commands
    def test_d_test_command_error_ignore_save(self):
        command = 'test_command_error'

        MMCScript.objects.create(name=command, ignore=True, save_on_error=True)
        self.__test_command(command, False)
        self.__check_email()
