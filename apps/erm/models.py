# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from treebeard.mp_tree import MP_Node

from treebeard.al_tree import AL_Node

from treebeard.ns_tree import NS_Node

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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


class Rubricator(models.Model):
    name = models.CharField(max_length=128, verbose_name=_(u"Rubricator name"))
    vendor = models.CharField(max_length=128, verbose_name=_(u"Rubricator's vendor"))
    comments = models.TextField(max_length=2048, verbose_name=_(u"Comments"), blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("name", "vendor")


class LocalRubric(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'), db_index=True)
    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'))
    linked = models.BooleanField(verbose_name=u'Имеет ли связь', default=False, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("name", "parent")


class ExtendedRubric(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'), db_index=True)
    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'))
    linked = models.BooleanField(verbose_name=u'Имеет ли связь', default=False, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("name", "parent")


class Rubric(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'), db_index=True)
    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'))
    linked = models.BooleanField(verbose_name=u'Имеет ли связь', default=False, db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("name", "parent")
        ordering = ['name']


class RubircLink(models.Model):
    local_rubric = models.ForeignKey(LocalRubric)
    ext_rubric = models.ForeignKey(ExtendedRubric)

    def __unicode__(self):
        return self.local_rubric.name + u' → ' + self.ext_rubric.name
#
#class Rubric(models.Model):
#
#    rubricator = models.ForeignKey(Rubricator, verbose_name=_(u"Rubricator"), db_index=True)
#    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'), db_index=True)
#    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'), default=True)
#    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
#
#    def __unicode__(self):
#        return self.name
#
#    class Meta:
#        unique_together = ("name", "parent", "rubricator")


#class Rubric(AL_Node):
#
#    rubricator = models.ForeignKey(Rubricator, verbose_name=_(u"Rubricator"), db_index=True)
#    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'), db_index=True)
#    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'), default=True)
#    parent = models.ForeignKey('self',
#                               related_name='children_set',
#                               null=True,
#                               db_index=True)
#    node_order_by = ['name']
#    def __unicode__(self):
#        return self.name




#
#import mptt
#from mptt.fields import TreeForeignKey
#
## add a parent foreign key
#TreeForeignKey(Rubric, blank=True, null=True).contribute_to_class(Rubric, 'parent')
#
#mptt.register(Group, order_insertion_by=['name'])



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







@receiver(post_save, sender=RubircLink)
def set_linked_flag(sender, instance, **kwargs):
    rubric = instance.local_rubric
    if not rubric.linked:
        rubric.linked = True
        rubric.save()

    rubric = instance.ext_rubric
    if not rubric.linked:
        rubric.linked = True
        rubric.save()


@receiver(post_delete, sender=RubircLink)
def unset_linked_flag(sender, instance, **kwargs):

    if RubircLink.objects.filter(local_rubric=instance.local_rubric).count() == 0:
        instance.local_rubric.linked = False
        instance.local_rubric.save()


    if RubircLink.objects.filter(ext_rubric=instance.ext_rubric).count() == 0:
        instance.ext_rubric.linked = False
        instance.ext_rubric.save()



#class Template(models.Model):
#    """
#    Шаблон/Запись. Отправная точка для конструктора
#    """
#    name = models.CharField(max_length=128, verbose_name=_(u'Template name'))
#
#    def __unicode__(self):
#        return self.name
#
#class ControlField(models.Model):
#    """
#    Контрольное поле
#    """
#    required = models.BooleanField(default=False, verbose_name=_(u"Required"))
#    template = models.ForeignKey(Template, verbose_name=_(u"Fields's owner template"))
#    tag = models.CharField( max_length=3, verbose_name=_(u'Filed tag'))
#    description = models.CharField(max_length=512, verbose_name=_(u'Field description'))
#
#    def __unicode__(self):
#        return self.tag
#
#    class Meta:
#        unique_together = ("template", "tag")
#
#
#class DataField(models.Model):
#    """
#    Поле данных.
#    Имеет набор значение для индикаторов 1 и 2, а так же набор подполей
#    """
#
#    template = models.ForeignKey(Template, verbose_name=_(u"Fields's owner template"))
#    tag = models.CharField(max_length=3, verbose_name=_(u'Filed tag'))
#
#    repeated = models.BooleanField(default=False, verbose_name=_(u"Repeated"))
#    required = models.BooleanField(default=False, verbose_name=_(u"Required"))
#
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    def __unicode__(self):
#        return self.tag
#
#    class Meta:
#        unique_together = ("template", "tag")
#
#
#class Indicator1(models.Model):
#    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Indicator's owner field"), null=True)
#    value = models.CharField( max_length=1, default=u' ', verbose_name=_(u'Value'))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("data_filed", "value")
#
#
#class Indicator2(models.Model):
#    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Indicator's owner field"), null=True)
#    value = models.CharField(max_length=1, default=u' ', verbose_name=_(u'Value'))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("data_filed", "value")
#
#
#class Subfield(models.Model):
#    """
#    Подполе поля
#    """
#    data_filed = models.ForeignKey(DataField, verbose_name=_(u"Subfield's owner field"))
#    code = models.CharField(max_length=1, verbose_name=_(u'Code'))
#    repeated = models.BooleanField(default=False, verbose_name=_(u"Repeated"))
#    required = models.BooleanField(default=False, verbose_name=_(u"Required"))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("data_filed", "code")
#
#class SubfieldPosition(models.Model):
#    """
#    Описание позиции подполя. Нпример поле 100 подполе a RUSMARC
#    """
#    subfield = models.ForeignKey(Subfield, verbose_name=_(u"Position's owner subfield"))
#    start_index = models.IntegerField(verbose_name=_(u"Position start index (first index - 1)"))
#    end_index = models.IntegerField(verbose_name=_(u"Position stop index (first index - 1)"))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("subfield", "start_index", "end_index")
#
#
#class Marker(models.Model):
#    """
#    Маркер шаблона
#    """
#    template = models.OneToOneField(Template, verbose_name=_(u"Markers's owner template"), unique=True)
#
#    def __unicode__(self):
#        return self.template.name + u'tempate marker'
#
#
#
#class MarkerPosition(models.Model):
#    """
#    Позиция маркера.
#    """
#    marker = models.ForeignKey(Marker, verbose_name=_(u"Position's owner marker"))
#    start_index = models.IntegerField(verbose_name=_(u"Position start index (first index - 1)"))
#    end_index = models.IntegerField(verbose_name=_(u"Position stop index (first index - 1)"))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("marker", "start_index", "end_index")
#
#
#class MarkerPositionValue(models.Model):
#    """
#    Значение позиции маркера
#    """
#    marker_position = models.ForeignKey(MarkerPosition, verbose_name=_(u"Value's owner marker position"))
#    value = models.CharField(max_length=24, verbose_name=_(u'Description'))
#    description = models.CharField(max_length=512, verbose_name=_(u'Description'))
#
#    class Meta:
#        unique_together = ("marker_position", "value")