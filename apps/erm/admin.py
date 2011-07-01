# -*- coding: utf-8 -*-
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from apps.erm.models import Rubric

admin.site.register(Rubric, MPTTModelAdmin)