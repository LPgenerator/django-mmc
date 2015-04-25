# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0009_auto_20150425_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='enable_queries',
            field=models.BooleanField(default=False, help_text=b'Profile queries numbers'),
        ),
    ]
