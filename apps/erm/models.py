from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

DATABASE_ENGINE = 'django.db.backends.sqlite3'

class BlobValueWrapper(object):
    """Wrap the blob value so that we can override the unicode method.
    After the query succeeds, Django attempts to record the last query
    executed, and at that point it attempts to force the query string
    to unicode. This does not work for binary data and generates an
    uncaught exception.
    """
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return  self.val

    def __unicode__(self):
        return  self.val


class BlobField(models.Field):
    """A field for persisting binary data in databases that we support."""
    __metaclass__ = models.SubfieldBase

    def db_type(self):

        if DATABASE_ENGINE == 'django.db.backends.mysql':
            return 'LONGBLOB'
        elif DATABASE_ENGINE == 'django.db.backends.postgresql_psycopg2':
            return 'bytea'
        elif DATABASE_ENGINE == 'django.db.backends.sqlite3':
            return 'BLOB'
        else:
            raise NotImplementedError

    def to_python(self, value):
        if DATABASE_ENGINE == 'django.db.backends.postgresql_psycopg2':
            if value is None:
                print value
                return value
            return str(value)
        else:
            return value

    def get_db_prep_save(self, value):
        if value is None:
            return None
        if DATABASE_ENGINE =='django.db.backends.postgresql_psycopg2':
            return psycopg2.Binary(value)
        else:
            return value

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
    name = models.CharField(max_length=256, verbose_name=_(u"Organisation name"))
    description = models.TextField(max_length=2048, verbose_name=_(u"Description"))



class License(models.Model):
    organisation = models.ForeignKey(Organisation, verbose_name=_(u'Organisation'))
    start_date = models.DateTimeField(verbose_name=_(u'Start date'))
    end_date = models.DateTimeField(verbose_name=_(u'End date'))
    access_rules = models.CharField(choices=ACCESS_RULES, max_length=32, verbose_name=_(u'Access rules'))
    terms = models.TextField(verbose_name=_(u'License terms'))



class DataBase(models.Model):
    license = models.ForeignKey(License, verbose_name=_(u'License'))
    name = models.CharField(max_length=256, verbose_name=_(u"Database name"))


class Resource(models.Model):
    database = models.ForeignKey(DataBase, verbose_name=_(u'Database'))
    record = models.TextField(max_length=102400,verbose_name=_(u'Record body (base64'))
    record_syntax = models.CharField(choices=RECORD_SYNTAXES, max_length=32, verbose_name=_(u'Record body'))


class Rubric(MPTTModel):
    name = models.CharField(max_length=128, verbose_name=_(u'Rubric name'))
    show = models.BooleanField(verbose_name=_(u'Show or hide rubric'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    def __unicode__(self):
        return self.name