# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MMCEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now=True)),
                ('email', models.EmailField(help_text=b'Email will be used for send all exceptions from command.', max_length=75)),
                ('is_active', models.BooleanField(default=True, help_text=b'Email may be switched off for a little while.')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MMCHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('ignore', models.BooleanField(default=False, help_text=b'All logs from all scripts on this host will be ignored.')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MMCLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(auto_now=True)),
                ('elapsed', models.FloatField()),
                ('success', models.NullBooleanField(default=None)),
                ('error_message', models.TextField(null=True, blank=True)),
                ('traceback', models.TextField(null=True, blank=True)),
                ('sys_argv', models.CharField(max_length=255, null=True, blank=True)),
                ('memory', models.FloatField(default=0.0)),
                ('cpu_time', models.FloatField(default=0.0)),
                ('hostname', models.ForeignKey(to='mmc.MMCHost')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MMCScript',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('ignore', models.BooleanField(default=False, help_text=b'All logs from this script will be ignored.')),
                ('one_copy', models.BooleanField(default=False, help_text=b'Only one copy of this script will be run.')),
                ('save_on_error', models.BooleanField(default=False, help_text=b'This flag used only for ignored commands.')),
            ],
            options={
                'verbose_name': 'Script',
                'verbose_name_plural': 'Scripts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mmclog',
            name='script',
            field=models.ForeignKey(to='mmc.MMCScript'),
            preserve_default=True,
        ),
    ]
