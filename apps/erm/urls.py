# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.erm',
    url(r'^bv/(?P<year>\d+)/$', 'views_frontend.BaseView', name="erm_bv"),
    url(r'^$', 'views_frontend.index', name="erm_index"),
    url(r'^detail/$', 'views_frontend.resource_detail', name="erm_resource_detail"),
    url(r'^rs/$', 'views_frontend.rubrics_select', name="erm_rubrics_select"),
    url(r'^slr/$', 'views_frontend.search_local_rubrics', name="erm_search_local_rubrics"),
    url(r'^ser/$', 'views_frontend.search_ext_rubrics', name="erm_search_ext_rubrics"),
    url(r'^glri/$', 'views_frontend.get_local_rubric_info', name="erm_get_local_rubric_info"),
    url(r'^geri/$', 'views_frontend.get_ext_rubric_info', name="erm_get_ext_rubric_info"),
    url(r'^srl/$', 'views_frontend.save_rubric_links', name="erm_save_rubric_links"),
    url(r'^rc/$', 'views_frontend.rubric_cloud', name="erm_rubric_cloud"),
    url(r'^rrc/$', 'views_frontend.render_rubric_cloud', name="erm_render_rubric_cloud"),



    #url(r'^detail/pdf/$', 'resource_detail_pdf',  name="erm_resource_detail_pdf"),
    url(r'^search/$', 'views_frontend.search_resources', name="erm_search_resources"),
    url(r'^admin/$', 'views_admin.index', name="erm_admin_index"),



    url(r'^admin/databases/$', 'views_admin.databases', name="erm_admin_databases"),
    url(r'^admin/databases/detail/(?P<id>\d+)/$', 'views_admin.database_detail', name="erm_admin_database_detail"),
    url(r'^admin/databases/edit/(?P<id>\d+)/$', 'views_admin.database_edit', name="erm_admin_database_edit"),
    url(r'^admin/databases/delete/(?P<id>\d+)/$', 'views_admin.database_delete', name="erm_admin_database_delete"),
    url(r'^admin/databases/create/$', 'views_admin.create_databases', name="erm_admin_create_databases"),

    url(r'^admin/licences/$', 'views_admin.licenses', name="erm_admin_licences"),
    url(r'^admin/licences/create/$', 'views_admin.license_create', name="erm_admin_licence_create"),



    url(r'^admin/rubrics/$', 'views_admin.rubrics', name="erm_admin_rubrics"),
    url(r'^admin/rubrics/linked/$', 'views_admin.linked', name="erm_admin_linked"),
    url(r'^admin/rubrics/rubricators/$', 'views_admin.rubricators', name="erm_admin_rubricators"),
    url(r'^admin/rubrics/rubricators/create/$', 'views_admin.rubricator_create', name="erm_admin_rubricator_create"),
    url(r'^admin/rubrics/loadfile/$', 'views_admin.load_rubrics_file', name="erm_admin_load_rubrics_file"),
)
