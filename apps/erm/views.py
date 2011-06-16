#coding: utf-8
from django.utils.translation import ugettext as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect

from libs import pyaz
import libs.pymarc as pymarc
import appsettings

journals_base = appsettings.ZBASES['journals']
zconnection = pyaz.ZConnection(
    {
        'user': journals_base['server']['user'],
        'password':journals_base['server']['password'],
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
    search_results = []
    if 'term' in request.GET:
        zresults = zconnection.search(u'@attr 1=4 %s' % 'Philosophy')
        search_results = []
        offset = 0
        number = offset # порядковый номер записи в результате
        print zresults.get_size()
        for zrecord in zresults.get_records(offset, 20):
            number += 1
            search_results.append(
                {
                    'number': number,
                    'record': pymarc.Record(data=zrecord,to_unicode=True, encoding='utf-8')
                }
            )
    
    return render_to_response(
        'index.html',
        {
            'message': _('Hello'),
            'search_results': search_results,
        },
        context_instance=RequestContext(request)
    )