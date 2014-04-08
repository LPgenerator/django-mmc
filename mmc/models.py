__author__ = 'gotlium'

from django.db import models


class MMCHost(models.Model):
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    ignore = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'

    def __unicode__(self):
        return self.name


class MMCScript(models.Model):
    created = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    ignore = models.BooleanField(default=False)

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
