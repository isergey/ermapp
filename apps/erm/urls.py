# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.erm',
    url(r'^$', 'views.index', name="erm_index"),
    url(r'^detail/$', 'views.resource_detail', name="erm_resource_detail"),
    #url(r'^detail/pdf/$', 'resource_detail_pdf',  name="erm_resource_detail_pdf"),
    url(r'^search/$', 'views.search_resources', name="erm_search_resources"),

)
