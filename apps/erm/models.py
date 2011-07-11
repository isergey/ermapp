# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


ACCESS_RULES = (
        ('ip', u'IP'),
        ('password', u'Password'),
        ('free', u'Free'),
    )

RESOURCE_TYPES = (
        ('journal', u'Journal'),
    )

RECORD_SYNTAXES = (
        ('xml', u'XML'),
        ('rusmarc', u'RUSMARC'),
        ('usmarc', u'USMARC'),
        ('unimarc', u'UNIMARC'),
    )

class Organisation(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"Organisation name"))
    description = models.TextField(max_length=2048, verbose_name=_(u"Description"))

    def __unicode__(self):
        return self.name


class License(models.Model):
    organisation_name = models.CharField(max_length=255, verbose_name=_(u"Organisation name"))
    name = models.CharField(max_length=255, verbose_name=_(u"Licence name"), unique=True)
    start_date = models.DateTimeField(verbose_name=_(u'Start date'), db_index=True)
    end_date = models.DateTimeField(verbose_name=_(u'End date'), db_index=True)
    access_rules = models.CharField(choices=ACCESS_RULES, max_length=32, verbose_name=_(u'Access rules'))
    terms = models.TextField(verbose_name=_(u'License terms'))

    def __unicode__(self):
        return self.name + ' / ' + self.organisation.name


class Rubric(MPTTModel):
    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'))
    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name


class Database(models.Model):
    license = models.ForeignKey(License, verbose_name=_(u'License'))
    name = models.CharField(max_length=255, verbose_name=_(u"Database name"))
    rubrics = models.ManyToManyField(Rubric)

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    database = models.ForeignKey(Database, verbose_name=_(u'Database'))
    record = models.TextField(max_length=102400, verbose_name=_(u'Record body (base64'))
    record_syntax = models.CharField(choices=RECORD_SYNTAXES, max_length=32, verbose_name=_(u'Record body'))


class Template(models.Model):
    """
    Шаблон/Запись. Отправная точка для конструктора
    """
    name = models.CharField(max_length=128, verbose_name=_(u'Template name'))

    def __unicode__(self):
        return self.name

class ControlField(models.Model):
    """
    Контрольное поле
    """
    required = models.BooleanField(default=False, verbose_name=_(u"Required"))
    template = models.ForeignKey(Template, verbose_name=_(u"Fields's owner template"))
    tag = models.CharField( max_length=3, verbose_name=_(u'Filed tag'))
    description = models.CharField(max_length=512, verbose_name=_(u'Field description'))

    def __unicode__(self):
        return self.tag

    class Meta:
        unique_together = ("template", "tag")


class DataField(models.Model):
    """
    Поле данных.
    Имеет набор значение для индикаторов 1 и 2, а так же набор подполей
    """

    template = models.ForeignKey(Template, verbose_name=_(u"Fields's owner template"))
    tag = models.CharField(max_length=3, verbose_name=_(u'Filed tag'))

    repeated = models.BooleanField(default=False, verbose_name=_(u"Repeated"))
    required = models.BooleanField(default=False, verbose_name=_(u"Required"))

    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    def __unicode__(self):
        return self.tag

    class Meta:
        unique_together = ("template", "tag")


class Indicator1(models.Model):
    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Indicator's owner field"), null=True)
    value = models.CharField( max_length=1, default=u' ', verbose_name=_(u'Value'))
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("data_filed", "value")


class Indicator2(models.Model):
    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Indicator's owner field"), null=True)
    value = models.CharField(max_length=1, default=u' ', verbose_name=_(u'Value'))
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("data_filed", "value")


class Subfield(models.Model):
    """
    Подполе поля
    """
    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Subfield's owner field"))
    code = models.CharField(max_length=1, verbose_name=_(u'Code'))
    repeated = models.BooleanField(default=False, verbose_name=_(u"Repeated"))
    required = models.BooleanField(default=False, verbose_name=_(u"Required"))   
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("data_filed", "code")

class SubfieldPosition(models.Model):
    """
    Описание позиции подполя. Нпример поле 100 подполе a RUSMARC
    """
    subfield = models.ForeignKey(Subfield, verbose_name=_(u"Position's owner subfield"))
    start_index = models.IntegerField(verbose_name=_(u"Position start index (first index - 1)"))
    end_index = models.IntegerField(verbose_name=_(u"Position stop index (first index - 1)"))
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("subfield", "start_index", "end_index")


class Marker(models.Model):
    """
    Маркер шаблона
    """
    template = models.OneToOneField(Template, verbose_name=_(u"Markers's owner template"), unique=True)

    def __unicode__(self):
        return self.template.name + u'tempate marker'



class MarkerPosition(models.Model):
    """
    Позиция маркера.
    """
    marker = models.ForeignKey(Marker, verbose_name=_(u"Position's owner marker"))
    start_index = models.IntegerField(verbose_name=_(u"Position start index (first index - 1)"))
    end_index = models.IntegerField(verbose_name=_(u"Position stop index (first index - 1)"))
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("marker", "start_index", "end_index")


class MarkerPositionValue(models.Model):
    """
    Значение позиции маркера
    """
    marker_position = models.ForeignKey(MarkerPosition, verbose_name=_(u"Value's owner marker position"))
    value = models.CharField(max_length=24, verbose_name=_(u'Description'))
    description = models.CharField(max_length=512, verbose_name=_(u'Description'))

    class Meta:
        unique_together = ("marker_position", "value")