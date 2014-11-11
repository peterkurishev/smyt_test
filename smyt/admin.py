# -*- coding: utf-8 -*-

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


def auto_register():
    for model in apps.get_app_config('smyt').get_models():
        if not model._meta.abstract:
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass

auto_register()