#coding: utf-8
from django.conf import settings
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect

from libs import pyaz
import libs.pymarc as pymarc
import appsettings

import pymorphy

en_morph = pymorphy.get_morph(settings.SYSTEM_ROOT+'appdata/pymorphy/dicts/en','cdb')
ru_morph = pymorphy.get_morph(settings.SYSTEM_ROOT+'appdata/pymorphy/dicts/ru','cdb')


journals_base = appsettings.ZBASES['journals']
zconnection = pyaz.ZConnection(
        {
        'user': journals_base['server']['user'],
        'password': journals_base['server']['password'],
        'databaseName': journals_base['server']['databaseName'],
        'preferredRecordSyntax': journals_base['server']['preferredRecordSyntax'],
        }
)

zconnection.connect(str(journals_base['server']['host']), int(journals_base['server']['port']))

def index(request):
    return render_to_response(
        'index.html',
            {'message': _('Hello')},
        context_instance=RequestContext(request)
    )



def search_resources(request):
    USE_ATTRIBUTES = {
        'anywhere':u'1035',
        'author': u'1003',
        'title': u'4',
        'subject': u'21',
    }
    search_results = []

    if 'term' in request.GET \
        and request.GET['term'] \
        and 'use' in request.GET \
        and request.GET['use'] in USE_ATTRIBUTES:

        terms = request.GET['term'].split()
        use = USE_ATTRIBUTES[request.GET['use']]

        lemmas = []
        qb = pyaz.RPNQueryBuilder()
        if 'ft'not in request.GET:
            for term in terms:
                en_words =  en_morph.decline(term.upper())
                for en_word in en_words:
                    lemmas.append(en_word['word'])
                if en_words:
                    lemmas.append(en_words[0]['lemma'])
                    qb.add_condition(term=en_words[0]['lemma'].lower(), use=use, structure=u"6", truncation=u'3')

            for term in terms:
                ru_words = ru_morph._decline(term.upper())
                for i, ru_word in enumerate(ru_words):
                    #    print ru_word['lemma']
                    lemmas.append(ru_word['word'])

                if ru_words:
                    lemmas.append(ru_words[0]['lemma'])
                    qb.add_condition(term=ru_words[0]['lemma'].lower(), use=use, structure=u"6", truncation=u'3')

            query = qb.build()
        else:
            qb.add_condition(term=request.GET['term'], use=use)
            query = qb.build()
        
        print query, type(query)
        zresults = zconnection.search(query)
        search_results = []
        offset = 0
        number = offset # порядковый номер записи в результате
        from time import time as t

        for zrecord in zresults.get_records(offset, 20):
            number += 1
            record = pymarc.Record(data=zrecord, to_unicode=True, encoding='utf-8')
            #print record
            texts = record['200']['a'].split()
            record.remove_field(record['200'])

            for i in xrange(len(texts)):
                for lemma in lemmas:

                    if texts[i].find(lemma.upper()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]
                    if texts[i].find(lemma.lower()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]
                    if texts[i].find(lemma.lower().capitalize()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]

                for term in terms:
                    if texts[i].find(term.upper()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]
                    if texts[i].find(term.lower()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]
                    if texts[i].find(term.lower().capitalize()) != -1:
                        texts[i] = '<span style="color: green">%s</span>' % texts[i]
            record.add_field(pymarc.Field(tag='200', indicators=(' ', ' '), subfields=('a',' '.join(texts))))

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
            'message': _('Hello'),
            'search_results': search_results,
            'request': request
            },
        context_instance=RequestContext(request)
    )