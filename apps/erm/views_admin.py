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
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError


from libs import pyaz, filework
import libs.pymarc as pymarc
import appsettings
from models import Resource, Rubric
from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm

from forms import LicenseForm, RubricFileForm, RubricatorForm

from models import License, Rubricator, LocalRubric, Rubric, RubircLink
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

def licenses(request):
    licenses  = License.objects.all()
    paginator = Paginator(licenses, 1)

    page = request.GET.get('page',1)
    try:
        licenses_list = paginator.page(page)
    except PageNotAnInteger:
        licenses_list = paginator.page(1)
    except EmptyPage:
        licenses_list = paginator.page(paginator.num_pages)

    return render_to_response(
        'admin_licenses_list.html',
        {
            'licenses_list': licenses_list,
            'module':'erm',
            'tab':'license'
        },
        context_instance=RequestContext(request)
    )



def license_create(request):

    if request.method == 'POST':
        form = LicenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erm_admin_licences')
    else:
        form = LicenseForm()

    return render_to_response(
        'admin_license_create.html',
        {
            'form': form,
            'module':'erm',
            'tab':'license'
        },
        context_instance=RequestContext(request)
    )


def rubricators(request):
    rubricators  = Rubricator.objects.all()
    paginator = Paginator(rubricators, 1)

    page = request.GET.get('page',1)
    try:
        rubricators_list = paginator.page(page)
    except PageNotAnInteger:
        rubricators_list = paginator.page(1)
    except EmptyPage:
        rubricators_list = paginator.page(paginator.num_pages)

    return render_to_response(
        'admin_rubricators_list.html',
        {
            'rubricators_list': rubricators_list,
            'module':'erm',
            'tab':'rubrics'
        },
        context_instance=RequestContext(request)
    )

def rubricator_create(request):

    if request.method == 'POST':
        form = RubricatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erm_admin_rubricators')
    else:
        form = RubricatorForm()

    return render_to_response(
        'admin_rubricator_create.html',
        {
            'form': form,
            'module':'erm',
            'tab':'rubrics'
        },
        context_instance=RequestContext(request)
    )

def rubrics(request):
    #root = Rubric.objects.get(name=u'root')
    root= Rubric.objects.get(name='root')
    rubrics = root.children.all()[0:10]

#    tree = []
    for rubric in rubrics:
        print rubric.children.all()
        
    #print rubrics
    return render_to_response(
        'admin_rubricator_create.html',
        {
#            'form': 'form',
            'module':'erm',
            'tab':'rubrics'
        },
        context_instance=RequestContext(request)
    )


def linked(request):
    local_rubric = LocalRubric.objects.get(name=u'Физика')
    links = RubircLink.objects.filter(local_rubric=local_rubric)
    for link in links:
        print link.local_rubric, link.ext_rubric.get_children()
    
    return HttpResponse(u'edede')


def load_rubrics_file(request):
    """
    Загрузка файла с рубриками
    """

    if request.method == 'POST':
        form = RubricFileForm(request.POST, request.FILES)
        if form.is_valid():
            rubricator = get_object_or_404(Rubricator, pk=form.cleaned_data['rubricator'])
            print rubricator
            extract_rubric_handler(request.FILES['file'],
                                   rubricator,
                                   form.cleaned_data['syntax'],
                                   form.cleaned_data['type'],
                                   form.cleaned_data['encoding']
            )

    else:
        form = RubricFileForm()

    return render_to_response(
        'admin_load_rubrics_file.html',
        {
            'form': form,
            'message': _('Licences'),
            'module':'erm',
            'tab':'rubrics'
        },
        context_instance=RequestContext(request)
    )



from django.db import connection
from time import time as t
@transaction.commit_manually
def extract_rubric_handler(upload_file, rubricator, syntax, type, encoding):

    get = lambda node_id: Rubric.objects.get(pk=node_id)

    file_path  = filework.save_content_to_file(upload_file, settings.SYSTEM_ROOT+'appdata/tmp/', file_ext='mrc')
    records = []
    s = t()
    #root = Rubric.add_root(name='root', rubricator=rubricator)
#    roots = Rubric.get_root_nodes()
#
#    if not roots:
#        root = Rubric.add_root(name='root', rubricator=rubricator)
#    else:
#        root = roots[0]
#    print root


    #node = get(root.id).add_child(name='Memory', rubricator=rubricator)
    #print node
    #node = get(root.id).add_child(name='CPU', rubricator=rubricator)
    #node.add_child(name='PENTIUM', rubricator=rubricator)
    #node = Rubric.objects.get(name=u'PENTIUM', rubricator=rubricator)
    #print node
   #print Rubric.dump_bulk()
    try:
        root = Rubric.objects.get(name=rubricator.name, parent=None)
    except Rubric.DoesNotExist:
        root = Rubric(name=rubricator.name, parent=None)
        root.save()

#    rubric = Rubric(name=u'dddd')
#    rubric.insert_at(root)
#    root.save()
#    return
#    rubric = Rubric(name=u'Физика', parent=root, rubricator=rubricator)
#    rubric.save()
#
#    rubric = Rubric(name=u'Ядерная', parent=rubric, rubricator=rubricator)
#    rubric.save()
#
#    return



    if syntax == 'USMARC':
        reader = pymarc.MARCReader(file(file_path), encoding=encoding, to_unicode=True)
    else:
        reader = pymarc.UNIMARCReader(file(file_path), encoding=encoding, to_unicode=True)

        for i, record in enumerate(reader):
#            rubric = None
#            if record['606']:
#                rubric = record['606']['a']
#
#            print record['100']['a'], rubric
#            continue
            fields = record.get_fields('606')
            for field in fields:
                rubric_name = field['a'].strip(' .')

                if rubric_name:

                    try:
                        rubric = Rubric.objects.get(name=rubric_name, parent=root)
                    except Rubric.DoesNotExist:
                        rubric = Rubric(name=rubric_name, parent=root)
                        rubric.save()
                        #rubric = root.add_child(name=rubric_name,rubricator=rubricator)

                    subrubrics = field.get_subfields('x')
                    if len(subrubrics):
                        for subrubric_name in subrubrics:
                            subrubric_name = subrubric_name.strip(' .')

                            try:
                                subrubric = Rubric.objects.get(name=subrubric_name, parent=rubric)
                            except Rubric.DoesNotExist:
                                subrubric = Rubric(name=subrubric_name, parent=rubric)
                                subrubric.save()
                                #rubric.add_child(name=subrubric_name, rubricator=rubricator)

            if i % 50 ==  0:
                transaction.commit()
                print 'commit'
            print i

#                    print 'sb:', subrubric_name, rubric_name

    transaction.commit()
    print Rubric.objects.all().count()
    print 'time:', t() - s

    
#from django.db import connection
#from time import time as t
#@transaction.commit_manually
#def extract_rubric_handler(upload_file, rubricator, syntax, type, encoding):
#
#    cursor = connection.cursor()
#
#    cach = {}
#    file_path  = filework.save_content_to_file(upload_file, settings.SYSTEM_ROOT+'appdata/tmp/', file_ext='mrc')
#    records = []
#    s = t()
#    try:
#        root = Rubric.objects.get(name=u'root', parent=None)
#    except Rubric.DoesNotExist:
#        root = Rubric(name=u'root', parent=None)
#        root.save()
#
#
#
#    if syntax == 'USMARC':
#        reader = pymarc.MARCReader(file(file_path), encoding=encoding, to_unicode=True)
#    else:
#        reader = pymarc.UNIMARCReader(file(file_path), encoding=encoding, to_unicode=True)
#
#        for i, record in enumerate(reader):
#            fields = record.get_fields('606')
#            for field in fields:
#                rubric_name = field['a'].strip(' .')
#
#                if rubric_name:
#                    cursor.execute("SELECT id FROM erm.erm_rubric WHERE name = %s and parent_id = %s",
#                        [rubric_name, root.pk])
#                    rubric = cursor.fetchone()
#                    if not rubric:
#                        cursor.execute("INSERT INTO erm.erm_rubric (name, `show`, parent_id) VALUES(%s, %s, %s)",
#                            [rubric_name,True, root.pk])
#                        rubric = cursor.execute("SELECT LAST_INSERT_ID()")
#                        rubric = cursor.fetchone()
#
#                    subrubrics = field.get_subfields('x')
#                    if len(subrubrics):
#                        for subrubric_name in subrubrics:
#                            subrubric_name = subrubric_name.strip(' .')
#                            cursor.execute("INSERT INTO erm.erm_rubric (name, `show`, parent_id ) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)",
#                                [subrubric_name, True, rubric[0]])
#                            print 'insert-------------------'
#            print i
#
##                    print 'sb:', subrubric_name, rubric_name
#
#    transaction.commit()
#    print Rubric.objects.all().count()
#    print 'time:', t() - s
