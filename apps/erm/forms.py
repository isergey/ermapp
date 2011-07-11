# coding: utf-8

from django.forms import ModelForm
from models import License

class LicenseForm(ModelForm):
    class Meta:
        model = License
