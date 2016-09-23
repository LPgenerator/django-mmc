# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0015_auto_20160706_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='last_call',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 23, 12, 51, 43, 352472, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mmcscript',
            name='max_elapsed',
            field=models.FloatField(default=0.0),
        ),
    ]
