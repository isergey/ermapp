# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import forms
from models import License, Rubricator
from django.forms.extras.widgets import SelectDateWidget



class MultiTextField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        super(MultiTextField, self).__init__(*args, **kwargs)
    def compress(self, data_list):
        print data_list

class DatabaseForm(forms.Form):
    name = forms.CharField(label=_(u'Database name'), max_length=256)
    vendor = forms.CharField(label=(u'Vendor'), max_length=256)
    rubrics = forms.CharField(label=_(u'Rubric name'), max_length=256)

    descriprion = forms.CharField(label=(u'Descriprion'), max_length=256, widget=forms.Textarea, required=False)

    start_date = forms.DateField(label=(u'Start date'), widget=SelectDateWidget)
    end_date = forms.DateField(label=(u'End date'), widget=SelectDateWidget)
    

class RubricForm(forms.Form):
    name = forms.CharField(label=_(u'Rubric name'), max_length=256)
    


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License


RUBRIC_FILE_SYNTAXES = (
    ('rusmarc', 'RUSMARC'),
    ('usmarc', 'USMARC'),
    ('unimarc', 'UNIMARC'),
)


RUBRIC_FILE_TYPES = (
    ('bibliographic', _('Bibliographic')),
    ('authoritative', _('Authoritative')),
)

ENCODINGS = (
    ('UTF-8', 'UTF-8'),
    ('cp1251', 'Windows-1251'),
    ('koi8-r', 'koi8-r'),
    ('latin-1', 'Latin-1'),
    ('marc8', 'marc8'),
)

def get_rubricators_choices():
    choices = []
    rubricators = Rubricator.objects.all()
    for rubricator in rubricators:
        choices.append((rubricator.pk, rubricator.name))
    return choices


class RubricatorForm(forms.ModelForm):
    class Meta:
        model = Rubricator

class RubricFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RubricFileForm, self).__init__(*args, **kwargs)
        self.fields['rubricator'] = forms.ChoiceField(choices=get_rubricators_choices())
        
    rubricator = forms.ChoiceField(label=_(u'Rubricator'))
    syntax = forms.ChoiceField(choices=RUBRIC_FILE_SYNTAXES, label=_(u'File syntax'))
    type = forms.ChoiceField(choices=RUBRIC_FILE_TYPES, label=_(u'File type'))
    encoding = forms.ChoiceField(choices=ENCODINGS, label=_(u'Records encoding'))
    file  = forms.FileField(label=_(u'Select file '))
    