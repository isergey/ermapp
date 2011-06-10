# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse, Http404, HttpResponseRedirect

def set_lang(request):
    return direct_to_template(request, 'setlang_form.html')

def index(request):
    return HttpResponse( _('Hello'))