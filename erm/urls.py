# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('erm.views',
    url(r'^$', 'index', name="erm_index"),
    url(r'^setlang/$', 'set_lang', name="erm_set_lang"),
)
