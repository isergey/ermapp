# encoding: utf-8 -*-
import re
import difflib
import pymorphy
from lxml import etree
from time import time as t
import simplejson
import StringIO
import logging

from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms.models import model_to_dict
from view import View

from libs import pyaz
import libs.pymarc as pymarc
import appsettings
from models import Resource, LocalRubric, RubircLink, ExtendedRubric, Rubric
from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


en_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/en', 'cdb')
ru_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/ru', 'cdb')

term_word_split_re = re.compile(ur'\W+', re.UNICODE)
latin_letters_re = re.compile(ur'^[a-zA-Z]+$', re.UNICODE)
russian_letters_re = re.compile(ur'^[а-яА-Я]+$', re.UNICODE)

full_xslt_root = etree.parse(settings.SYSTEM_ROOT + 'appdata/xslt/marc.xsl')
full_transform = etree.XSLT(full_xslt_root)


def lcs(S1, S2):
    """
    Поиск наибольшей общей последовательности в двух строках
    """
    M = [[0] * (1 + len(S2)) for i in xrange(1 + len(S1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(S1)):
        for y in xrange(1, 1 + len(S2)):
            if S1[x - 1] == S2[y - 1]:
                M[x][y] = M[x - 1][y - 1] + 1
                if M[x][y] > longest:
                    longest = M[x][y]
                    x_longest = x
            else:
                M[x][y] = 0
    return S1[x_longest - longest: x_longest]


def lcs_from_word_list(word_list, min_length=3):
    """
    Поиск наибольшей общей последовательности в списке слов
    """
    lcses = []
    min_length = 3
    for i in xrange(len(word_list)):
        common = lcs(word_list[0], word_list[i])
        if len(common) >= min_length:
            lcses.append((common, len(common)))

    if not lcses: return u""

    lcses = sorted(lcses, key=lambda x: x[1])

    return lcses[0][0]


def lemma_search(words, min_term_length):
    """
    Поиск леммы нужной длины
    """
    #если лемма слова нужной длины, то используем ее
    if len(words[0]['lemma']) >= min_term_length:
        return words[0]['lemma']

    #иначе, подбираем лемму нужной длины
    else:
        word_list = []
        for word in words:
            word_list.append(word['word'])

        lcs_lemma = lcs_from_word_list(word_list, min_term_length)

        if lcs_lemma:
            return lcs_lemma

    return u""


def highlighting(words, record, filed='200', subfield='a' ):
    """
    Подсветка найденных слов.
    Пока подсвечивает только первое поле и подполе
    """
    texts = record[filed][subfield].split()
    record.remove_field(record[filed])

    for i in xrange(len(texts)):
        for word in words:
            if texts[i].find(word.upper()) != -1:
                texts[i] = '<span style="color: green">%s</span>' % texts[i]
            if texts[i].find(word.lower()) != -1:
                texts[i] = '<span style="color: green">%s</span>' % texts[i]
            if texts[i].find(word.lower().capitalize()) != -1:
                texts[i] = '<span style="color: green">%s</span>' % texts[i]

    record.add_field(pymarc.Field(tag=filed, indicators=(' ', ' '), subfields=(subfield, ' '.join(texts))))
    return record


class BaseView(View):
    #обработка пост запроса
    def post(self):
        request = self.request #используем объект request
        return self.render_to_response('index.html', {'a': 'a', 'b': 'b'})

    #обработка запроса, если нет методов для post или get
    def do(self, year):
        return self.render_to_response('index.html', {'a': 'a', 'b': 'b'})


def index(request):
#    resource = Resource(record='ededwedwed', record_syntax='XML')
#    resource.save()
    logger = logging.getLogger('file_logger')
    logger.error(u'Вызов индекса')
    import sys

    #    rubrics_tree = Rubric.tree.filter(show=True)
    reader = pymarc.MARCReader(file(settings.SYSTEM_ROOT + 'appdata/rusmarc_ebsco.mrc'), encoding='utf-8',
                               to_unicode=True)
    records = []
    i = 0
    for record in reader:
        print str(record.as_marc())
        i += 1
        if i > 10: break
        records.append(pymarc.record_to_dict(record=record))
        #print simplejson.dumps(pymarc.record_to_dict(record=record), encoding='utf-8', ensure_ascii=False)
    #    print 'ok'
    #print simplejson.dumps(records, ensure_ascii=False ,encoding='utf-8')
    print sys.getsizeof(pymarc)
    #simplejson.dump(records, , ensure_ascii=False, encoding='utf-8')
    #print simplejson.dumps(records, ensure_ascii=False, encoding='utf-8')

    file(settings.SYSTEM_ROOT + 'appdata/rusmarc_ebsco.json', 'wb').write(
        simplejson.dumps(records, encoding='utf-8', ensure_ascii=False, sort_keys=True, indent=4).encode('utf-8'))
    records = simplejson.load(file(settings.SYSTEM_ROOT + 'appdata/rusmarc_ebsco.json', 'rb'))
    for record in records:
        print record['datafields']['200'][0]['subfields']['a'][0]

    return render_to_response(
        'index.html',
            {'message': _('Hello'),
             },
        context_instance=RequestContext(request)
    )


def search_resources(request):
    journals_base = appsettings.ZBASES['journals']
    zconnection = pyaz.ZConnection(
        journals_base['server']
    )

    zconnection.connect(str(journals_base['server']['host']), int(journals_base['server']['port']))
    USE_ATTRIBUTES = {
        'anywhere': u'1035',
        'author': u'1003',
        'title': u'4',
        'subject': u'21',
        }
    search_results = []

    #print request.GET.urlencode()

    term = request.GET.get('term', None)
    use = request.GET.get('use', None)
    ft = request.GET.get('ft', None)
    min_term_length = appsettings.SEARCH['min_term_length']

    if use and use in  USE_ATTRIBUTES:
        use = USE_ATTRIBUTES[use]
    else:
        use = None

    term_count = 0
    zrecords = None

    if term and not ft:
        #разбиваем терм на слова
        terms = re.split(term_word_split_re, term)

        fuzzy_terms = [] #список нечетких термов
        for trm in terms:
            #определяем принадлежность слова к русскому языку
            if re.match(russian_letters_re, trm):
                ru_words = ru_morph.decline(trm.upper())
                searched_lemma = lemma_search(ru_words, min_term_length)
                if searched_lemma:
                    fuzzy_terms.append(searched_lemma)

            #определяем принадлежность слова к англ языку
            elif re.match(latin_letters_re, trm):
                en_words = en_morph.decline(trm.upper())
                searched_lemma = lemma_search(en_words, min_term_length)
                if searched_lemma:
                    fuzzy_terms.append(searched_lemma)
            else:
                if len(trm) >= min_term_length:
                    fuzzy_terms.append(trm)

        term_count = len(fuzzy_terms)

        query_builder = pyaz.RPNQueryBuilder()

        query_builder.add_condition(term=u' '.join(fuzzy_terms), use=use, structure=u"6", truncation=u'3')

        query = query_builder.build()
        print query
    elif term and ft:
        term_count = 1
        query_builder = pyaz.RPNQueryBuilder()
        query_builder.add_condition(term=term, use=use)
        query = query_builder.build()
        fuzzy_terms = term.split()

    if term_count:
        zresults = None
        #try:
        zresults = zconnection.search(query)
        #except Exception:
        #    pass

        if zresults:
            paginator = Paginator(object_list=zresults, per_page=10)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            try:
                zrecords = paginator.page(page)
            except (EmptyPage, InvalidPage):
                zrecords = paginator.page(paginator.num_pages)
            print zrecords
            search_results = []
            offset = page * paginator.per_page - paginator.per_page
            number = offset # порядковый номер записи в результате

            for zrecord in zrecords.object_list:
                number += 1
                record = pymarc.Record(data=zrecord, to_unicode=True, encoding='utf-8')
                record.add_field(pymarc.Field(tag='993', indicators=(' ', ' '), subfields=('a', record.as_md5(),)))
                record = highlighting(fuzzy_terms, record)
                #print record
                search_results.append(
                        {
                        'number': number,
                        'record': record.as_dict()
                    }
                )



                #print search_results[-1]['record']

    return render_to_response(
        'index.html',
            {
            'test': {'rec': [{'ee': 'ggg'}]},
            'search_url': request.GET.urlencode(),
            'search_results': search_results,
            'pages_list': zrecords,
            },
        context_instance=RequestContext(request)
    )


def resource_detail(request):
    journals_base = appsettings.ZBASES['journals']
    zconnection = pyaz.ZConnection(
        journals_base['server']
    )

    zconnection.connect(str(journals_base['server']['host']), int(journals_base['server']['port']))
    search_url = request.GET.get('search_url', None)
    resource_id = request.GET.get('id', None)

    if not resource_id:
        raise Http404(_(u'Resource not founded'))

    query_builder = pyaz.RPNQueryBuilder()
    query_builder.add_condition(term=resource_id, use=u'12')
    query = query_builder.build()
    zresults = zconnection.search(query)
    if not len(zresults):
        raise Http404(_(u'Resource not founded'))
    print zresults.get_record(0)
    zrecord = zresults[0]
    record = pymarc.UnimarcRecord(data=zrecord, to_unicode=True, encoding='utf-8')
    print simplejson.dumps(pymarc.record_to_dict(record), encoding='utf-8', ensure_ascii=False)
    doc = etree.XML(pymarc.record_to_rustam_xml(record))
    #print pymarc.record_to_rustam_xml(record)
    result_tree = full_transform(doc)
    full_document = unicode(result_tree)

    return render_to_response(
        'detail.html',
            {
            'record': record.as_dict(),
            'full_document': full_document,
            'search_url': search_url,
            },
        context_instance=RequestContext(request)
    )


def bibliograph(request):
    return render_to_response(
        'bibliograph.html',
        context_instance=RequestContext(request)
    )


def rubric_path(node):
    path_list = [node]
    #print node.get_ancestors()
    parent = node.parent
    while parent:
        path_list.append(parent)
        parent = parent.parent
    return path_list


def rubrics_select(request):
    rubricators = ExtendedRubric.objects.filter(parent=None)
    return render_to_response(
        'link_rubrics.html',
            {
            'rubricators': rubricators,
            },
        context_instance=RequestContext(request)
    )


def search_local_rubrics(request):
    rubric_name = request.GET.get('name', None)
    page = request.GET.get('page', 0)

    local_rubrics = LocalRubric.objects.filter(name__icontains=rubric_name).exclude(parent=None).order_by('name')
    paginator = Paginator(local_rubrics, 20)
    try:
        local_rubrics_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        local_rubrics_list = paginator.page(paginator.num_pages)

    pathes = []

    for rubric in local_rubrics_list.object_list:
        ancestors = rubric_path(rubric) #rubric.get_ancestors(ascending=True)
        row = []
        for ancestor in  ancestors[:-1]:
            ancestor_dict = model_to_dict(ancestor)
            ancestor_dict['is_leaf_node'] = ancestor.is_leaf_node()
            row.insert(0, ancestor_dict)
            #row.append(model_to_dict(rubric))
        pathes.append(row)
    return HttpResponse(simplejson.dumps(pathes, encoding='utf-8', ensure_ascii=False))


def search_ext_rubrics(request):
    rubric_name = request.GET.get('name', None)
    rubricator = request.GET.get('rubricator', None)
    print rubricator
    pathes = []

    if rubric_name:
        rubrics = ExtendedRubric.objects.filter(name__icontains=rubric_name, tree_id=int(rubricator)).exclude(
            parent=None)
        for rubric in rubrics:
            ancestors = rubric.get_ancestors(ascending=True)
            row = []
            for ancestor in  ancestors:
                if ancestor.is_root_node(): break
                row.append(model_to_dict(ancestor))
            row.append(model_to_dict(rubric))
            pathes.append(row)

    return HttpResponse(simplejson.dumps(pathes, encoding='utf-8', ensure_ascii=False))


def get_local_rubric_info(request):
    rubric_id = request.GET.get('id', None)
    result = []
    try:
        rubric = LocalRubric.objects.get(pk=rubric_id)
        ancestors = rubric_path(rubric)[:-1]
        for ancestor in rubric_path(rubric)[:-1]:
            result.insert(0, model_to_dict(ancestor))
    except LocalRubric.DoesNotExist:
        pass
    print result
    return HttpResponse(simplejson.dumps(result, encoding='utf-8', ensure_ascii=False))


def get_ext_rubric_info(request):
    rubric_id = request.GET.get('id', None)
    result = {
        'path': [],
        'rubricator': None
    }
    try:
        rubric = ExtendedRubric.objects.get(pk=rubric_id)
        ancestors = rubric_path(rubric)[:-1]
        for ancestor in rubric_path(rubric)[:-1]:
            result['path'].insert(0, model_to_dict(ancestor))
    except ExtendedRubric.DoesNotExist:
        pass

    try:
        rubricator = ExtendedRubric.objects.get(parent=None, tree_id=rubric.tree_id)
        result['rubricator'] = model_to_dict(rubricator)
    except ExtendedRubric.DoesNotExist:
        pass

    return HttpResponse(simplejson.dumps(result, encoding='utf-8', ensure_ascii=False))


#from django import http
#from django.shortcuts import render_to_response
#from django.template.loader import get_template
#from django.template import Context
#import xhtml2pdf.pisa as pisa
#import cStringIO as StringIO
#import cgi
#
#
#
#def render_to_pdf(template_src, context_dict):
#    template = get_template(template_src)
#    context = Context(context_dict)
#    html  = template.render(context)
#    result = StringIO.StringIO()
#    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
#    if not pdf.err:
#        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
#    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
#
#def resource_detail_pdf(request):
#
#
#    journals_base = appsettings.ZBASES['journals']
#    zconnection = pyaz.ZConnection(
#        journals_base['server']
#    )
#
#    zconnection.connect(str(journals_base['server']['host']), int(journals_base['server']['port']))
#    search_url = request.GET.get('search_url', None)
#    resource_id = request.GET.get('id', None)
#
#    if not resource_id:
#        raise Http404(_(u'Resource not founded'))
#
#
#
#    query_builder = pyaz.RPNQueryBuilder()
#    query_builder.add_condition(term=resource_id, use=u'12')
#    query = query_builder.build()
#    zresults = zconnection.search(query)
#    if not len(zresults):
#        raise Http404(_(u'Resource not founded'))
#    print zresults.get_record(0)
#    zrecord = zresults[0]
#    record = pymarc.UnimarcRecord(data=zrecord, to_unicode=True, encoding='cp1251')
#
#    doc = etree.XML(pymarc.record_to_rustam_xml(record))
#    #print pymarc.record_to_rustam_xml(record)
#    result_tree = full_transform(doc)
#    full_document = unicode(result_tree)
#    return render_to_pdf(        'detail.html',
#            {
#            'record': record,
#            'full_document': full_document,
#            'search_url': search_url,
#            },
#    )
#{'datafields': [
#{'i1': ' ', 'tag': '011', 'subfields': [{'code': 'a', 'data': u'1557-4989'}], 'i2': ' '},
#{'i1': ' ', 'tag': '035', 'subfields': [{'code': 'a', 'data': u'(EbpS)ebs49725450'}], 'i2': ' '},
#{'i1': ' ', 'tag': '100', 'subfields': [{'code': 'a', 'data': u'20070321a    9999u  y0engy01020304ba'}], 'i2': ' '},
#{'i1': '|', 'tag': '101', 'subfields': [{'code': 'a', 'data': u'eng'}], 'i2': ' '},
#{'i1': ' ', 'tag': '110', 'subfields': [{'code': 'a', 'data': u'auu    0uu0'}], 'i2': ' '},
#{'i1': '1', 'tag': '200', 'subfields': [{'code': 'a', 'data': u'American Journal of Agricultural & Biological Science'}, {'code': 'b', 'data': u'[electronic resource].'}], 'i2': ' '},
#{'i1': ' ', 'tag': '210', 'subfields': [{'code': 'a', 'data': u'New York'}, {'code': 'c', 'data': u'Science Publications'}], 'i2': ' '},
#{'i1': ' ', 'tag': '300', 'subfields': [{'code': 'a', 'data': u'Academic Journal'}], 'i2': ' '},
#{'i1': ' ', 'tag': '310', 'subfields': [{'code': 'a', 'data': u'Indexing and abstracting for print publication.'}], 'i2': ' '},
#{'i1': ' ', 'tag': '463', 'subfields': [{'code': '1', 'datafields': [{'i1': '1', 'tag': '200', 'subfields': [{'code': 'a', 'data': u'Academic Search Complete '}], 'i2': ' '}]}, {'code': '1', 'datafields': [{'i1': ' ', 'tag': '210', 'subfields': [{'code': 'a', 'data': u'Ipswich, MA '}, {'code': 'c', 'data': u' EBSCO Publishing'}, {'code': 'd', 'data': u'1999-'}], 'i2': ' '}]}], 'i2': '1'}, {'i1': ' ', 'tag': '801', 'subfields': [{'code': 'a', 'data': u'RU'}, {'code': 'b', 'data': u'ORGANIZATION'}, {'code': 'c', 'data': u'20110608'}], 'i2': ' '}, {'i1': '4', 'tag': '856', 'subfields': [{'code': '3', 'data': u'Abstracts Available: Oct 2006- '}, {'code': 'z', 'data': u'Available on EBSCOhost.'}, {'code': 'u', 'data': u'http://search.ebscohost.com/direct.asp?db=a9h&jid=%221H62%22&scope=site'}], 'i2': '0'}], 'controlfields': [{'tag': '001', 'data': '473'}, {'tag': '001', 'data': '473'}, {'tag': '005', 'data': '20110608180224.0'}], 'leader': '00771cas a22002053i 450 ', 'syntax': u'1.2.840.10003.5.28'}
"""
{
    "datafields": {
        "200":
            [
                {
                    "i1": "1",
                    "i2": " ",
                    "subfields": {
                        "a": ["American journal of transplantation"],
                        "b": ["[electronic resource]"],
                        "e": ["official journal of the Amociety of Transplant Surgeons."]
                    }
                }
            ],
        "856":
            [
                {
                    "i1": "4",
                    "i2": "0",
                    "subfields": {
                        "3": ["Full text available: May 2001-. (he most recent 12  available.). "],
                        "z": ["Available on EBSCOhost."],
                        "u": ["http://search.ebscohost.com/direct.asp?db=a9h&jid=%22HXS%22&scope=site"]
                    }
                }
            ],
        "606":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Transplantation of organs, tissues, etc."],
                        "x": ["Periodicals."]
                    }
                },
                {
                    "i1": "1",
                    "i2": " ",
                    "subfields": {
                        "a": ["Transplantation"],
                        "x": ["Periodicals."]
                    }
                }
            ],
        "210":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Copenhagen, Denmark"],
                        "c": ["Munksgaard International Publishers"],
                        "d": ["2001"]
                    }
                }
            ],
        "207":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Vol. 1, issue 1 (May 2001)-"]
                    }
                }
            ],
        "300":
            [
                {"i1": " ",
                 "i2": " ",
                 "subfields": {
                     "a": ["Title from cover."]
                 }
                },
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Academic Journal"]
                    }
                }
            ],
        "310":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Online version of print publication."]
                    }
                }
            ],
        "712":
            [
                {
                    "i1": "0",
                    "i2": "2",
                    "subfields": {
                        "a": ["American Society of Transplantation."]
                    }
                },
                {
                    "i1": "0",
                    "i2": "2",
                    "subfields": {
                        "a": ["American Society of Transplant Surgeons."]
                    }
                }
            ],
        "463":
            [
                {
                    "i1": " ",
                    "i2": "1",
                    "subfields": {
                        "1": {
                                "datafields": {
                                    "210":
                                        [
                                            {
                                                "i1": " ",
                                                "i2": "1",
                                                "subfields": {
                                                    "a": ["Ipswich, MA "],
                                                    "c": [" EBSCO Publishing"],
                                                    "d": ["1999-"]
                                                }
                                            }
                                        ]
                                }
                        }
                    }
                }
            ],
        "307":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Has occasional supplements."]
                    }
                }
            ],
        "011":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["1600-6135"]
                    }
                }
            ],
        "326":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["Monthly,"],
                        "b": ["2003-"]
                    }
                }
            ],
        "110":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["afa    0uu0"]
                    }
                }
            ],
        "801":
            [
                {
                    "i1": " ",
                    "i2": "0",
                    "subfields": {
                        "a": ["DK"]
                    }
                },
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["RU"],
                        "c": ["20110608"],
                        "b": ["ORGANIZATION"]
                    }
                }
            ],
        "102":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["DK"]
                    }
                }
            ],
        "100":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["20010514a20019999u  y0engy01020304ba"]
                    }
                }
            ],
        "101":
            [
                {
                    "i1": "|",
                    "i2": " ",
                    "subfields": {
                        "a": ["eng"]
                    }
                }
            ],
        "680":
            [
                {
                    "i1": "0",
                    "i2": " ",
                    "subfields": {
                        "a": ["RD129.5"],
                        "b": [".A47"]
                    }
                }
            ],
        "035":
            [
                {
                    "i1": " ",
                    "i2": " ",
                    "subfields": {
                        "a": ["(EbpS)ebs728883"]
                    }
                }
            ]
    },
    "controlfields": {
        "001": "10042",
        "005": "20110608184508.0"
    },
    "leader": "01412cas a22003373i 450 ",
    "syntax": "1.2.840.10003.5.28"
}
"""
