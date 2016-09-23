# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0017_mmcscript_track_at_exit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmcscript',
            name='temporarily_disabled',
            field=models.SmallIntegerField(default=0, help_text=b'Temporarily disable script execution', choices=[(0, b'Enabled'), (1, b'Disabled / Raise error'), (2, b'Disabled / Silence mode')]),
        ),
    ]
