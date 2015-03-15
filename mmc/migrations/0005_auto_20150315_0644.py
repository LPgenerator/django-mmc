# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0004_mmcemail_ignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='enable_triggers',
            field=models.BooleanField(default=False, help_text=b'Enable triggers for receive email notification, if threshold of counters will be exceeded'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mmcscript',
            name='trigger_cpu',
            field=models.FloatField(help_text=b'Set the threshold time for CPU', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mmcscript',
            name='trigger_memory',
            field=models.FloatField(help_text=b'Set the threshold MB for Memory', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mmcscript',
            name='trigger_time',
            field=models.FloatField(help_text=b'Set the threshold sec for execution', null=True, blank=True),
            preserve_default=True,
        ),
    ]
