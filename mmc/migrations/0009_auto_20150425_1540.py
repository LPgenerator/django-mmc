# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0008_mmcscript_real_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmclog',
            name='queries',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mmcscript',
            name='save_on_error',
            field=models.BooleanField(default=False, help_text=b'This flag can be used only for ignored commands.'),
        ),
    ]
