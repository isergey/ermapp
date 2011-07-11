# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'License.organisation'
        db.delete_column('erm_license', 'organisation_id')

        # Adding field 'License.organisation_name'
        db.add_column('erm_license', 'organisation_name', self.gf('django.db.models.fields.CharField')(default='0', max_length=256), keep_default=False)

    def backwards(self, orm):
        
        # Adding field 'License.organisation'
        db.add_column('erm_license', 'organisation', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['erm.Organisation']), keep_default=False)

        # Deleting field 'License.organisation_name'
        db.delete_column('erm_license', 'organisation_name')

    models = {
        'erm.controlfield': {
            'Meta': {'unique_together': "(('template', 'tag'),)", 'object_name': 'ControlField'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Template']"})
        },
        'erm.database': {
            'Meta': {'object_name': 'Database'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rubrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['erm.Rubric']", 'symmetrical': 'False'})
        },
        'erm.datafield': {
            'Meta': {'unique_together': "(('template', 'tag'),)", 'object_name': 'DataField'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Template']"})
        },
        'erm.indicator1': {
            'Meta': {'unique_together': "(('data_filed', 'value'),)", 'object_name': 'Indicator1'},
            'data_filed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.DataField']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '1'})
        },
        'erm.indicator2': {
            'Meta': {'unique_together': "(('data_filed', 'value'),)", 'object_name': 'Indicator2'},
            'data_filed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.DataField']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "u' '", 'max_length': '1'})
        },
        'erm.license': {
            'Meta': {'object_name': 'License'},
            'access_rules': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'terms': ('django.db.models.fields.TextField', [], {})
        },
        'erm.marker': {
            'Meta': {'object_name': 'Marker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['erm.Template']", 'unique': 'True'})
        },
        'erm.markerposition': {
            'Meta': {'unique_together': "(('marker', 'start_index', 'end_index'),)", 'object_name': 'MarkerPosition'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'end_index': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Marker']"}),
            'start_index': ('django.db.models.fields.IntegerField', [], {})
        },
        'erm.markerpositionvalue': {
            'Meta': {'unique_together': "(('marker_position', 'value'),)", 'object_name': 'MarkerPositionValue'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marker_position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.MarkerPosition']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '24'})
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
        },
        'erm.subfield': {
            'Meta': {'unique_together': "(('data_filed', 'code'),)", 'object_name': 'Subfield'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'data_filed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.DataField']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'erm.subfieldposition': {
            'Meta': {'unique_together': "(('subfield', 'start_index', 'end_index'),)", 'object_name': 'SubfieldPosition'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'end_index': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_index': ('django.db.models.fields.IntegerField', [], {}),
            'subfield': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Subfield']"})
        },
        'erm.template': {
            'Meta': {'object_name': 'Template'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['erm']
