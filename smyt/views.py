import json

from django.apps import apps
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder

from smyt.forms import create_dynamic_form


def index(request):
    """
    View function to get smyt application index page with list of models.

    :param request: Not used
    :return:        Output template with models list
    """
    all_models = [dict([('name', m.__name__), ('title', m._meta.verbose_name.title())]) for m in
                  apps.get_app_config('smyt').get_models()]
    return render(request, 'smyt.html', {'models': all_models})


def get_data(request, model_name):
    """
    View function to get model metadata and records

    :param request:     Not used
    :param model_name:  Name of model to introspect and get data for
    :return:            JSON with model and records data
    """
    if request.is_ajax():
        model = apps.get_app_config('smyt').get_model(model_name)

        objects = [model_to_dict(o) for o in model.objects.all()]
        fields = [f.name for f in model._meta.fields]
        field_types = dict(zip(fields, [f.get_internal_type() for f in model._meta.fields]))
        field_titles = [f.verbose_name for f in model._meta.fields]

        result = {'objects': objects, 'fields': fields, 'field_titles': field_titles, 'field_types': field_types}
        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), content_type='application/json', status=200)
    else:
        return HttpResponse(status=401)


def get_form(request, model_name):
    """
    View function to get html representation of model object form. Too difficult to build it with JavaScript, sorry.

    :param request:     Not used
    :param model_name:  Name of model to build html form for
    :return:            HTML response of the form representation
    """

    if request.is_ajax():
        model = apps.get_app_config('smyt').get_model(model_name)
        form = create_dynamic_form(model)
        return render(request, 'form.html', {'form': form, 'model_name': model_name})
    else:
        return HttpResponse(status=401)


def add_record(request, model_name):
    """
    View function to manage record addition by model.

    :param request:     Used to get the form from request
    :param model_name:  Model name
    :return:            form if form is not valid, 200 code if form processed successfully.
    """
    if request.is_ajax():
        model = apps.get_app_config('smyt').get_model(model_name)
        form = create_dynamic_form(model)
        f = form(request.POST)
        if f.is_valid():
            o = f.save()
            return HttpResponse(json.dumps(model_to_dict(o), cls=DjangoJSONEncoder), content_type='application/json',
                                status=200)
        else:
            return render(request, 'form.html', {'form': f, 'model_name': model_name}, status=400)
    else:
        return HttpResponse(status=401)


def update_record(request, model_name):
    """
    View function to update model object record.

    :param request:     primary key, field name and new field data in request.POST
    :param model_name:  Name of model of the object record
    :return:            ok/nok
    """
    if request.is_ajax():
        model = apps.get_app_config('smyt').get_model(model_name)
        m = model.objects.get(pk=request.POST['pk'])
        field = request.POST['field']
        value = request.POST['value']
        m.__dict__.update({field: value})

        try:
            m.clean_fields()
        except ValidationError:
            return HttpResponse(status=400)

        m.save(update_fields=[field])

        return HttpResponse(json.dumps('ok'), content_type='application/json', status=200)
    else:
        return HttpResponse(status=401)