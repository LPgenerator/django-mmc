# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmc', '0016_auto_20160923_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmcscript',
            name='track_at_exit',
            field=models.BooleanField(default=True, help_text=b'Disable for uWSGI/Celery'),
        ),
    ]
