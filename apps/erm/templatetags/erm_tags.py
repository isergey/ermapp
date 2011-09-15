# -*- coding: utf-8 -*-
from django import template
from django.core.cache import cache
from ..models import TermCount

register = template.Library()

@register.inclusion_tag('cloud.html')
def rubric_cloud(max_count=50):
    tags = []
    if not tags:
        terms = TermCount.objects.filter(count__gt=10).order_by('?')[0:max_count]
        max_count = 0

        for term in terms:
            if term.count > max_count: max_count = term.count

        for term in terms:
            tags.append({'tag':term.term, 'size': "%.0f" % round((term.count * 20 / max_count / 1.0))})

        tags = sorted(tags, key=lambda x: x['tag'])

#    cache.set('tags', tags, 60)
    return { 'tags': tags }