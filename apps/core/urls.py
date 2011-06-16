# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('apps.core.views',
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', 'index', name="core_index"),
    url(r'^selang/$', 'select_lang', name="core_select_lang"),
)
