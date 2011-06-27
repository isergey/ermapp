#coding: utf-8
import re
import difflib
import pymorphy
from time import time as t

from django.conf import settings
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from libs import pyaz
import libs.pymarc as pymarc
import appsettings


en_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/en', 'cdb')
ru_morph = pymorphy.get_morph(settings.SYSTEM_ROOT + 'appdata/pymorphy/dicts/ru', 'cdb')

term_word_split_re = re.compile(ur'\W+', re.UNICODE)
latin_letters_re = re.compile(ur'^[a-zA-Z]+$', re.UNICODE)
russian_letters_re = re.compile(ur'^[а-яА-Я]+$', re.UNICODE)

journals_base = appsettings.ZBASES['journals']
zconnection = pyaz.ZConnection(
    journals_base['server']
)

zconnection.connect(str(journals_base['server']['host']), int(journals_base['server']['port']))


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


def index(request):
    return render_to_response(
        'index.html',
            {'message': _('Hello')},
        context_instance=RequestContext(request)
    )


def search_resources(request):
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
        use =  USE_ATTRIBUTES[use]
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

                texts = record['200']['a'].split()
                record.remove_field(record['200'])

                for i in xrange(len(texts)):
                    for term in fuzzy_terms:
                        if texts[i].find(term.upper()) != -1:
                            texts[i] = '<span style="color: green">%s</span>' % texts[i]
                        if texts[i].find(term.lower()) != -1:
                            texts[i] = '<span style="color: green">%s</span>' % texts[i]
                        if texts[i].find(term.lower().capitalize()) != -1:
                            texts[i] = '<span style="color: green">%s</span>' % texts[i]

                record.add_field(pymarc.Field(tag='200', indicators=(' ', ' '), subfields=('a', ' '.join(texts))))

                search_results.append(
                        {
                        'number': number,
                        'record': record
                    }
                )



                #print search_results[-1]['record']

    return render_to_response(
        'index.html',
            {
            'search_url': request.GET.urlencode(),
            'search_results': search_results,
            'pages_list': zrecords,
            },
        context_instance=RequestContext(request)
    )


def resource_detail(request):
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
    record = pymarc.Record(data=zrecord, to_unicode=True, encoding='utf-8')
    
    return render_to_response(
        'detail.html',
            {
            'record': record,
            'search_url': search_url,
            },
        context_instance=RequestContext(request)
    )