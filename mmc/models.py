__author__ = 'gotlium'

from django.core.mail import send_mail
from django.db import models
from django.conf import settings

from mmc.defaults import SUBJECT


class MMCHost(models.Model):
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    ignore = models.BooleanField(
        default=False,
        help_text='All logs from all scripts on this host will be ignored.')

    class Meta:
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'

    def __unicode__(self):
        return self.name


class MMCScript(models.Model):
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    ignore = models.BooleanField(
        default=False, help_text='All logs from this script will be ignored.')
    one_copy = models.BooleanField(
        default=False, help_text='Only one copy of this script will be run.')
    save_on_error = models.BooleanField(
        default=False, help_text='This flag used only for ignored commands.')

    @classmethod
    def get_one_copy(cls, name):
        return cls.objects.get(name=name).one_copy

    class Meta:
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'

    def __unicode__(self):
        return self.name


class MMCLog(models.Model):
    created = models.DateField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField(auto_now=True)
    elapsed = models.FloatField()
    hostname = models.ForeignKey(MMCHost)
    script = models.ForeignKey(MMCScript)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    sys_argv = models.CharField(max_length=255, blank=True, null=True)
    memory = models.FloatField(default=0.00)

    def __unicode__(self):
        return self.script.name

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    @classmethod
    def logging(cls, **kwargs):
        kwargs['script'] = MMCScript.objects.get_or_create(
            name=kwargs['script'])[0]
        kwargs['hostname'] = MMCHost.objects.get_or_create(
            name=kwargs['hostname'])[0]

        if not kwargs['script'].ignore and not kwargs['hostname'].ignore:
            cls.objects.create(**kwargs)
        elif not kwargs['success'] and kwargs['script'].save_on_error:
            cls.objects.create(**kwargs)


class MMCEmail(models.Model):
    created = models.DateField(auto_now=True, editable=False)
    email = models.EmailField(
        help_text='Email will be used for send all exceptions from command.')
    is_active = models.BooleanField(
        default=True,
        help_text='Email may be switched off for a little while.')

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    @classmethod
    def send(cls, message):
        try:
            emails = list(cls.objects.values_list(
                'email', flat=True).filter(is_active=True))
            if emails:
                send_mail(
                    SUBJECT, message, settings.DEFAULT_FROM_EMAIL, emails)
        except Exception, msg:
            print '[MMC]', msg.__unicode__()
