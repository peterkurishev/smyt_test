# -*- coding: utf-8 -*-
__author__ = 'Peter A. Kurishev'

# Django receipts snippet
from django import forms
from django.db import models


def create_dynamic_form(model):
    meta = type('Meta', (), {"model": model, })
    modelform_class = type('modelform', (forms.ModelForm,), {"Meta": meta, })
    for f in model._meta.fields:
        if type(f) == models.DateField:
            modelform_class.base_fields[f.name].widget.attrs['data-provide'] = 'datepicker'
    return modelform_class