# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MarkerPositionValue'
        db.create_table('erm_markerpositionvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('marker_position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.MarkerPosition'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['MarkerPositionValue'])

        # Adding unique constraint on 'MarkerPositionValue', fields ['marker_position', 'value']
        db.create_unique('erm_markerpositionvalue', ['marker_position_id', 'value'])

        # Adding model 'ControlField'
        db.create_table('erm_controlfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Template'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['ControlField'])

        # Adding unique constraint on 'ControlField', fields ['template', 'tag']
        db.create_unique('erm_controlfield', ['template_id', 'tag'])

        # Adding model 'Subfield'
        db.create_table('erm_subfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_filed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.DataField'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('repeated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['Subfield'])

        # Adding unique constraint on 'Subfield', fields ['data_filed', 'code']
        db.create_unique('erm_subfield', ['data_filed_id', 'code'])

        # Adding model 'DataField'
        db.create_table('erm_datafield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Template'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('repeated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['DataField'])

        # Adding unique constraint on 'DataField', fields ['template', 'tag']
        db.create_unique('erm_datafield', ['template_id', 'tag'])

        # Adding model 'Template'
        db.create_table('erm_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('erm', ['Template'])

        # Adding model 'Marker'
        db.create_table('erm_marker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Template'], unique=True)),
        ))
        db.send_create_signal('erm', ['Marker'])

        # Adding model 'MarkerPosition'
        db.create_table('erm_markerposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('marker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Marker'])),
            ('start_index', self.gf('django.db.models.fields.IntegerField')()),
            ('end_index', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['MarkerPosition'])

        # Adding unique constraint on 'MarkerPosition', fields ['marker', 'start_index', 'end_index']
        db.create_unique('erm_markerposition', ['marker_id', 'start_index', 'end_index'])

        # Adding model 'Indicator2'
        db.create_table('erm_indicator2', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_filed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.DataField'], null=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default=u' ', max_length=1)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['Indicator2'])

        # Adding unique constraint on 'Indicator2', fields ['data_filed', 'value']
        db.create_unique('erm_indicator2', ['data_filed_id', 'value'])

        # Adding model 'Indicator1'
        db.create_table('erm_indicator1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_filed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.DataField'], null=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default=u' ', max_length=1)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['Indicator1'])

        # Adding unique constraint on 'Indicator1', fields ['data_filed', 'value']
        db.create_unique('erm_indicator1', ['data_filed_id', 'value'])

        # Adding model 'SubfieldPosition'
        db.create_table('erm_subfieldposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subfield', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['erm.Subfield'])),
            ('start_index', self.gf('django.db.models.fields.IntegerField')()),
            ('end_index', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('erm', ['SubfieldPosition'])

        # Adding unique constraint on 'SubfieldPosition', fields ['subfield', 'start_index', 'end_index']
        db.create_unique('erm_subfieldposition', ['subfield_id', 'start_index', 'end_index'])

    def backwards(self, orm):
        
        # Removing unique constraint on 'SubfieldPosition', fields ['subfield', 'start_index', 'end_index']
        db.delete_unique('erm_subfieldposition', ['subfield_id', 'start_index', 'end_index'])

        # Removing unique constraint on 'Indicator1', fields ['data_filed', 'value']
        db.delete_unique('erm_indicator1', ['data_filed_id', 'value'])

        # Removing unique constraint on 'Indicator2', fields ['data_filed', 'value']
        db.delete_unique('erm_indicator2', ['data_filed_id', 'value'])

        # Removing unique constraint on 'MarkerPosition', fields ['marker', 'start_index', 'end_index']
        db.delete_unique('erm_markerposition', ['marker_id', 'start_index', 'end_index'])

        # Removing unique constraint on 'DataField', fields ['template', 'tag']
        db.delete_unique('erm_datafield', ['template_id', 'tag'])

        # Removing unique constraint on 'Subfield', fields ['data_filed', 'code']
        db.delete_unique('erm_subfield', ['data_filed_id', 'code'])

        # Removing unique constraint on 'ControlField', fields ['template', 'tag']
        db.delete_unique('erm_controlfield', ['template_id', 'tag'])

        # Removing unique constraint on 'MarkerPositionValue', fields ['marker_position', 'value']
        db.delete_unique('erm_markerpositionvalue', ['marker_position_id', 'value'])

        # Deleting model 'MarkerPositionValue'
        db.delete_table('erm_markerpositionvalue')

        # Deleting model 'ControlField'
        db.delete_table('erm_controlfield')

        # Deleting model 'Subfield'
        db.delete_table('erm_subfield')

        # Deleting model 'DataField'
        db.delete_table('erm_datafield')

        # Deleting model 'Template'
        db.delete_table('erm_template')

        # Deleting model 'Marker'
        db.delete_table('erm_marker')

        # Deleting model 'MarkerPosition'
        db.delete_table('erm_markerposition')

        # Deleting model 'Indicator2'
        db.delete_table('erm_indicator2')

        # Deleting model 'Indicator1'
        db.delete_table('erm_indicator1')

        # Deleting model 'SubfieldPosition'
        db.delete_table('erm_subfieldposition')

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
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Organisation']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'terms': ('django.db.models.fields.TextField', [], {})
        },
        'erm.marker': {
            'Meta': {'object_name': 'Marker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['erm.Template']", 'unique': 'True'})
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
