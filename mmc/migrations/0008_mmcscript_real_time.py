# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0007_mmcscript_calls'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='real_time',
            field=models.BooleanField(default=False, help_text=b'Real Time info about command (for long tasks).'),
        ),
    ]
