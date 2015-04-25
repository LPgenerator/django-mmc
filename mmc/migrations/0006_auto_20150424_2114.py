# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0005_auto_20150315_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmclog',
            name='pid',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='mmcemail',
            name='email',
            field=models.EmailField(help_text=b'Email will be used for send all exceptions from command.', max_length=254),
        ),
    ]
