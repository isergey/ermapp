# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.erm',
    url(r'^$', 'views_frontend.index', name="erm_index"),
    url(r'^detail/$', 'views_frontend.resource_detail', name="erm_resource_detail"),
    #url(r'^detail/pdf/$', 'resource_detail_pdf',  name="erm_resource_detail_pdf"),
    url(r'^search/$', 'views_frontend.search_resources', name="erm_search_resources"),
    url(r'^admin/$', 'views_admin.index', name="erm_admin_index"),
)
