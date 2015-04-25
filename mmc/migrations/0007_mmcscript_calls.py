# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0006_auto_20150424_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='calls',
            field=models.BigIntegerField(default=0, verbose_name=b'Number of calls'),
        ),
    ]
