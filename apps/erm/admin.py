# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin
from apps.erm import models
from treebeard.admin import TreeAdmin

admin.site.register(models.Rubric, MPTTModelAdmin)

admin.site.register(models.LocalRubric, MPTTModelAdmin)

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Organisation,OrganisationAdmin)

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date')

admin.site.register(models.License,LicenseAdmin)

class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Database,DatabaseAdmin)



class RubricatorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Rubricator ,RubricatorAdmin)


class RubircLinkAdmin(admin.ModelAdmin):
    list_display = ('local_rubric','ext_rubric')
admin.site.register(models.RubircLink ,RubircLinkAdmin)

#class RubricAdmin(TreeAdmin):
#    list_display = ('name',)
#
#admin.site.register(models.Rubric ,RubricAdmin)



#
#
#class TemplateAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#
#admin.site.register(models.Template,TemplateAdmin)
#
#
#
#
#class ControlFieldAdmin(admin.ModelAdmin):
#    list_display = ('tag','description')
#
#admin.site.register(models.ControlField, ControlFieldAdmin)
#
#
#class DataFieldAdmin(admin.ModelAdmin):
#    list_display = ('tag','description')
#
#admin.site.register(models.DataField, DataFieldAdmin)
#
#
#
#class Indicator1Admin(admin.ModelAdmin):
#    list_display = ('data_filed','value','description')
#
#admin.site.register(models.Indicator1, Indicator1Admin)
#
#
#class Indicator2Admin(admin.ModelAdmin):
#    list_display = ('data_filed','value','description')
#
#admin.site.register(models.Indicator2, Indicator2Admin)
#
#
#class SubfieldAdmin(admin.ModelAdmin):
#    list_display = ('data_filed','code','description')
#
#admin.site.register(models.Subfield, SubfieldAdmin)
#
#
#class SubfieldPositionAdmin(admin.ModelAdmin):
#    list_display = ('subfield','start_index','end_index','description')
#
#admin.site.register(models.SubfieldPosition, SubfieldPositionAdmin)
#
#
#class MarkerAdmin(admin.ModelAdmin):
#    list_display = ('template', )
#
#admin.site.register(models.Marker, MarkerAdmin)
#
#
#class MarkerPositionAdmin(admin.ModelAdmin):
#    list_display = ('marker', 'start_index', 'end_index', 'description')
#
#admin.site.register(models.MarkerPosition, MarkerPositionAdmin)
#
#
#class MarkerPositionValueAdmin(admin.ModelAdmin):
#    list_display = ('marker_position', 'value', 'description')
#
#admin.site.register(models.MarkerPositionValue, MarkerPositionValueAdmin)
#    organisation = models.ForeignKey(Organisation, verbose_name=_(u'Organisation'))
#    start_date = models.DateTimeField(verbose_name=_(u'Start date'))
#    end_date = models.DateTimeField(verbose_name=_(u'End date'))
#    access_rules = models.CharField(choices=ACCESS_RULES, max_length=32, verbose_name=_(u'Access rules'))
#    terms = models.TextField(verbose_name=_(u'License terms'))