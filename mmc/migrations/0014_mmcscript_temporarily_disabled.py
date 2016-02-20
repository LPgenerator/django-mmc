# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0013_mmclog_is_fixed'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='temporarily_disabled',
            field=models.BooleanField(default=False, help_text=b'Temporarily disable script execution'),
        ),
    ]
