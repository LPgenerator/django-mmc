# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0012_auto_20150717_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmclog',
            name='is_fixed',
            field=models.NullBooleanField(default=None),
        ),
    ]
