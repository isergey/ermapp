# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Resource.database'
        db.alter_column('erm_resource', 'database_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Database']))

        # Adding M2M table for field rubrics on 'Database'
        db.create_table('erm_database_rubrics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('database', models.ForeignKey(orm['erm.database'], null=False)),
            ('rubric', models.ForeignKey(orm['erm.rubric'], null=False))
        ))
        db.create_unique('erm_database_rubrics', ['database_id', 'rubric_id'])

    def backwards(self, orm):
        
        # Changing field 'Resource.database'
        db.alter_column('erm_resource', 'database_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.DataBase']))

        # Removing M2M table for field rubrics on 'Database'
        db.delete_table('erm_database_rubrics')

    models = {
        'erm.database': {
            'Meta': {'object_name': 'Database'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rubrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['erm.Rubric']", 'symmetrical': 'False'})
        },
        'erm.license': {
            'Meta': {'object_name': 'License'},
            'access_rules': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Organisation']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
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
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Database']"}),
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
