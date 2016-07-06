# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0014_mmcscript_temporarily_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmcemail',
            name='ignore',
            field=models.ManyToManyField(help_text=b'Helpful for different teams. Choose script which you want to ignore.', to='mmc.MMCScript', blank=True),
        ),
    ]
