# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0002_mmclog_was_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmclog',
            name='stdout_messages',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
