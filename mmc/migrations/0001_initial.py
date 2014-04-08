# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MMCHost'
        db.create_table('mmc_mmchost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mmc', ['MMCHost'])

        # Adding model 'MMCScript'
        db.create_table('mmc_mmcscript', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('mmc', ['MMCScript'])

        # Adding model 'MMCLog'
        db.create_table('mmc_mmclog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('elapsed', self.gf('django.db.models.fields.FloatField')()),
            ('hostname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmc.MMCHost'])),
            ('script', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mmc.MMCScript'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('traceback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sys_argv', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('mmc', ['MMCLog'])


    def backwards(self, orm):
        
        # Deleting model 'MMCHost'
        db.delete_table('mmc_mmchost')

        # Deleting model 'MMCScript'
        db.delete_table('mmc_mmcscript')

        # Deleting model 'MMCLog'
        db.delete_table('mmc_mmclog')


    models = {
        'mmc.mmchost': {
            'Meta': {'object_name': 'MMCHost'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'mmc.mmclog': {
            'Meta': {'object_name': 'MMCLog'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'elapsed': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmc.MMCHost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'script': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mmc.MMCScript']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sys_argv': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'mmc.mmcscript': {
            'Meta': {'object_name': 'MMCScript'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['mmc']
