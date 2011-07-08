# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'License.name'
        db.add_column('erm_license', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'License.name'
        db.delete_column('erm_license', 'name')

    models = {
        'erm.database': {
            'Meta': {'object_name': 'DataBase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'erm.license': {
            'Meta': {'object_name': 'License'},
            'access_rules': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Organisation']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'terms': ('django.db.models.fields.TextField', [], {})
        },
        'erm.organisation': {
            'Meta': {'object_name': 'Organisation'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'erm.resource': {
            'Meta': {'object_name': 'Resource'},
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.DataBase']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.TextField', [], {'max_length': '102400'}),
            'record_syntax': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'erm.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['erm.Rubric']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['erm']
