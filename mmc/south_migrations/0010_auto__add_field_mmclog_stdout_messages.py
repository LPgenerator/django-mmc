# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MMCLog.stdout_messages'
        db.add_column('mmc_mmclog', 'stdout_messages',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MMCLog.stdout_messages'
        db.delete_column('mmc_mmclog', 'stdout_messages')


    models = {
        'mmc.mmcemail': {
            'Meta': {'object_name': 'MMCEmail'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mmc.mmchost': {
            'Meta': {'object_name': 'MMCHost'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mmc.mmclog': {
            'Meta': {'object_name': 'MMCLog'},
            'cpu_time': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'elapsed': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmc.MMCHost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmc.MMCScript']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'stdout_messages': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'sys_argv': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'was_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mmc.mmcscript': {
            'Meta': {'object_name': 'MMCScript'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'one_copy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'save_on_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mmc']