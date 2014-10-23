# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmclog',
            name='was_notified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
