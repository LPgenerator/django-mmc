# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0003_mmclog_stdout_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcemail',
            name='ignore',
            field=models.ManyToManyField(help_text=b'Helpful for different teams. Choose script which you want to ignore.', to='mmc.MMCScript', null=True, blank=True),
            preserve_default=True,
        ),
    ]
