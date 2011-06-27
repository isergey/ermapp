# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.erm.views',
    url(r'^$','index', name="erm_index"),
    url(r'^detail/$','resource_detail', name="erm_resource_detail"),
    url(r'^search/$','search_resources', name="erm_search_resources"),
    
)
