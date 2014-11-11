# -*- coding: utf-8 -*-
__author__ = 'Peter A. Kurishev'

from django.conf.urls import patterns, url

from smyt.views import index, get_data, get_form, add_record, update_record


urlpatterns = patterns('',
                       url(r'^$', index, name='index'),
                       url(r'^m/(?P<model_name>\w+)$', get_data, name='get_data'),
                       url(r'^f/(?P<model_name>\w+)$', get_form, name='get_form'),
                       url(r'a/(?P<model_name>\w+)$', add_record, name='add_record'),
                       url(r'u/(?P<model_name>\w+)$', update_record, name='update_record'),
)