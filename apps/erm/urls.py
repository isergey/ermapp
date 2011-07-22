# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.erm',
    url(r'^$', 'views_frontend.index', name="erm_index"),
    url(r'^detail/$', 'views_frontend.resource_detail', name="erm_resource_detail"),
    #url(r'^detail/pdf/$', 'resource_detail_pdf',  name="erm_resource_detail_pdf"),
    url(r'^search/$', 'views_frontend.search_resources', name="erm_search_resources"),
    url(r'^admin/$', 'views_admin.index', name="erm_admin_index"),
    url(r'^admin/licences/$', 'views_admin.licenses', name="erm_admin_licences"),
    url(r'^admin/licences/create/$', 'views_admin.license_create', name="erm_admin_licence_create"),
    
    url(r'^admin/rubrics/$', 'views_admin.rubrics', name="erm_admin_rubrics"),
    url(r'^admin/rubrics/linked/$', 'views_admin.linked', name="erm_admin_linked"),
    url(r'^admin/rubrics/rubricators/$', 'views_admin.rubricators', name="erm_admin_rubricators"),
    url(r'^admin/rubrics/rubricators/create/$', 'views_admin.rubricator_create', name="erm_admin_rubricator_create"),
    url(r'^admin/rubrics/loadfile/$', 'views_admin.load_rubrics_file', name="erm_admin_load_rubrics_file"),
)
