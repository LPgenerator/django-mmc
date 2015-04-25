# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0010_mmcscript_enable_queries'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='trigger_queries',
            field=models.FloatField(
                help_text=b'Set the threshold number of queries',
                null=True, blank=True),
        ),
    ]
