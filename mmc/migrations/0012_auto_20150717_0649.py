# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0011_auto_20150425_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='interval_restriction',
            field=models.PositiveIntegerField(default=None, help_text=b'Interval before script can be run again', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mmcscript',
            name='enable_queries',
            field=models.BooleanField(default=False, help_text=b'Profile queries numbers.'),
        ),
        migrations.AlterField(
            model_name='mmcscript',
            name='trigger_time',
            field=models.FloatField(help_text=b'Set the threshold sec for execution time', null=True, blank=True),
        ),
    ]
