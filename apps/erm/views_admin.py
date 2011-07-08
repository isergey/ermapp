# encoding: utf-8 -*-
import re
import difflib
import pymorphy
from lxml import etree
from time import time as t
import simplejson
import logging

from django.conf import settings
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from libs import pyaz
import libs.pymarc as pymarc
import appsettings
from models import Resource, Rubric
from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


#en_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/en', 'cdb')
#ru_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/ru', 'cdb')
#
#term_word_split_re = re.compile(ur'\W+', re.UNICODE)
#latin_letters_re = re.compile(ur'^[a-zA-Z]+$', re.UNICODE)
#russian_letters_re = re.compile(ur'^[а-яА-Я]+$', re.UNICODE)
#
#full_xslt_root = etree.parse(settings.SYSTEM_ROOT + 'appdata/xslt/marc.xsl')
#full_transform = etree.XSLT(full_xslt_root)


def index(request):

        
    return render_to_response(
        'admin_index.html',
        {
             'message': _('Hello'),
        },
        context_instance=RequestContext(request)
    )

