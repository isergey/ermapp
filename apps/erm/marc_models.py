# coding: utf-8
from libs import pymarc
import datetime
rusmarc_database_scheme = {
    'name': ('200', (' ', ' '), 'a'),
    'vendor': ('201', (' ', ' '), 'a'),
    'start_date': ('202', (' ', ' '), 'a'),
    'end_date': ('202', (' ', ' '), 'b'),
    'rubrics': ('606', (' ', ' '), 'a'),
    }

def field_constructor(scheme, item, data):
    """
    scheme - scheme dict
    item - item from scheme
    data - inserting data
    """
    if not isinstance(data, unicode):
        raise TypeError('data must be unicode string')

    field = pymarc.Field(
        tag=scheme[item][0],
        indicators=scheme[item][1],
        subfields=(scheme[item][2], data)
    )

    return field


class Database(object):
    def __init__(self, name, vendor, rubrics, start_date, end_date, id=None):
        self.id = id
        self.name = name
        self.vendor = vendor
        self.rubrics = rubrics
        self.start_date = start_date
        self.end_date = end_date

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, val):
        if not isinstance(val, datetime.date):
            raise TypeError('value must be datetime.date type')
        self.__start_date = val

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, val):
        if not isinstance(val, datetime.date):
            raise TypeError('value must be datetime.date type')
        self.__end_date = val

    def to_rusmarc(self):
        rusmarc_record = pymarc.Record()
        if self.id:
            rusmarc_record.add_field(pymarc.Field(
                tag='001', data=unicode(self.id)
            ))
        rusmarc_record.add_field(field_constructor(rusmarc_database_scheme, 'name', self.name))
        rusmarc_record.add_field(field_constructor(rusmarc_database_scheme, 'vendor', self.vendor))
        rusmarc_record.add_field(
                field_constructor(rusmarc_database_scheme, 'start_date', unicode(self.start_date.strftime('%Y%m%d')))
        )
        rusmarc_record.add_field(
            field_constructor(rusmarc_database_scheme, 'end_date', unicode(self.end_date.strftime('%Y%m%d')))
        )
        rusmarc_record.add_field(field_constructor(rusmarc_database_scheme, 'rubrics', self.rubrics))
        return rusmarc_record

    @classmethod
    def from_rusmarc(cls, record):
        if not isinstance(record, pymarc.Record):
            raise TypeError(u'Record must be pymarc.Record type')
        start_date = record.get_first_subfield(
            rusmarc_database_scheme['start_date'][0],
            rusmarc_database_scheme['start_date'][2]
        )

        end_date = record.get_first_subfield(
            rusmarc_database_scheme['end_date'][0],
            rusmarc_database_scheme['end_date'][2]
        )

        return Database(
            id=unicode(record['001'].data),
            name=unicode(record.get_first_subfield(
                rusmarc_database_scheme['name'][0],
                rusmarc_database_scheme['name'][2]
            )),
            vendor=unicode(record.get_first_subfield(
                rusmarc_database_scheme['vendor'][0],
                rusmarc_database_scheme['vendor'][2]
            )),
            start_date=datetime.datetime.strptime(start_date, '%Y%m%d').date(),
            end_date=datetime.datetime.strptime(end_date, '%Y%m%d').date(),
            rubrics=unicode(record.get_first_subfield(
                rusmarc_database_scheme['rubrics'][0],
                rusmarc_database_scheme['rubrics'][2]
            )),
        )

    def __unicode__(self):
        return self.name

    def __str__(self):
        if not isinstance(self.name, unicode):
            return self
        return self.name.encode('utf-8')