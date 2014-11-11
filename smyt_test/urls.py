# -*- coding: utf-8 -*-
__author__ = 'Peter A. Kurishev'

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
    url(r'^smyt/', include('smyt.urls', namespace='smyt')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^contacts/$', TemplateView.as_view(template_name='contacts.html'), name='contacts'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'),
                            )
