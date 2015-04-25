__author__ = 'gotlium'

from django.db import models
from django.utils.importlib import import_module

from mmc.defaults import SUBJECT, MAIL_MODULE, EMAIL_FROM


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
    calls = models.BigIntegerField('Number of calls', default=0)
    trigger_cpu = models.FloatField(
        null=True, blank=True, help_text='Set the threshold time for CPU')
    trigger_memory = models.FloatField(
        null=True, blank=True, help_text='Set the threshold MB for Memory')
    trigger_time = models.FloatField(
        null=True, blank=True, help_text='Set the threshold sec for execution')
    enable_triggers = models.BooleanField(
        default=False, help_text='Enable triggers for receive email '
                                 'notification, if threshold of counters '
                                 'will be exceeded')

    def update_calls(self):
        MMCScript.objects.filter(pk=self.pk).update(
            calls=models.F('calls') + 1)

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
    success = models.NullBooleanField(default=None)
    error_message = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    sys_argv = models.CharField(max_length=255, blank=True, null=True)
    memory = models.FloatField(default=0.00)
    cpu_time = models.FloatField(default=0.00)
    was_notified = models.BooleanField(default=False)
    stdout_messages = models.TextField(blank=True, null=True)
    pid = models.IntegerField(default=1)

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
        instance = kwargs.pop('instance', None)

        def do_save():
            if instance is not None:
                return cls.objects.filter(pk=instance.pk).update(**kwargs)
            kwargs.get('script').update_calls()
            return cls.objects.create(**kwargs)

        if not kwargs['script'].ignore and not kwargs['hostname'].ignore:
            return do_save()

        if kwargs['success'] is False and kwargs['script'].save_on_error:
            return do_save()

    @classmethod
    def get_lock_time(cls, script_name):
        return round(int(cls.objects.values_list(
            'elapsed', flat=True
        ).filter(script__name=script_name).order_by('-elapsed')[:1][0]) + 1)


class MMCEmail(models.Model):
    created = models.DateField(auto_now=True, editable=False)
    email = models.EmailField(
        help_text='Email will be used for send all exceptions from command.')
    ignore = models.ManyToManyField(
        MMCScript, blank=True, null=True,
        help_text='Helpful for different teams. '
                  'Choose script which you want to ignore.')
    is_active = models.BooleanField(
        default=True,
        help_text='Email may be switched off for a little while.')

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    @classmethod
    def send(cls, host_name, script_name, message, subject=SUBJECT):
        try:
            emails = list(cls.objects.values_list(
                'email', flat=True
            ).filter(is_active=True).exclude(ignore__name=script_name))
            if emails:
                subject = subject % dict(script=script_name, host=host_name)

                mail = import_module(MAIL_MODULE)
                mail.send_mail(
                    subject, message, EMAIL_FROM, emails, fail_silently=True
                )
        except Exception, msg:
            print '[MMC]', msg.__unicode__()
