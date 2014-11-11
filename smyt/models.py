# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# We are going to create models dynamically reading it from yaml file named "models.yaml"
from smyt import yaml_to_models, yaml_string_to_models


class SmytModelGenerator(object):
    """
    Custom model generator class.
    """

    def __init__(self, yaml_file=None):
        """
        Construct generator object. Fill it with file contents if file defined.

        :param yaml_file:   file name to get model structore from
        :return:            nothing
        """
        if yaml_file is None:
            self.models = []
        else:
            self.models = yaml_to_models(yaml_file)

    def init_from_string(self, yaml_string):
        """
        Init generator object from yaml string. For testing purposes.
        """
        self.models = yaml_string_to_models(yaml_string)

    def set_model_title(self, current_model):
        for field in self.models[current_model]['fields']:
            if field['type'] == 'char':
                return lambda self: u'%s' % self.__dict__[field['id']]
        return lambda self: u'%s №%d' % (current_model['title'], self.id)

    def create_dynamic_models(self):
        """
        Create models from model definition in models field. Check if model already registered (in case of test run)
        """
        for my_model in self.models:

            from django.apps import apps
            if my_model in apps.get_app_config('smyt').get_models():
                continue

            meta = type('Meta', (), {'verbose_name': self.models[my_model]['title'],
                                     'verbose_name_plural': self.models[my_model]['title']})
            attrs = {'__module__': self.__module__, '__unicode__': self.set_model_title(my_model), "Meta": meta}
            for field in self.models[my_model]['fields']:
                field_variants = {
                    'char': models.CharField(max_length=255, verbose_name=field['title']),
                    'int': models.IntegerField(verbose_name=field['title']),
                    'date': models.DateField(verbose_name=field['title']),
                    }

                attrs.update({field['id']: field_variants[field['type']]})
            try:
                from django.apps import apps
                model = apps.get_app_config('smyt').get_model(my_model)
                yield model
            except LookupError:
                model = type(my_model, (models.Model,), attrs)
                globals()[model.__name__] = model
                yield model

    def generate_models(self):
        return list(self.create_dynamic_models())


example_model_generator = SmytModelGenerator(settings.BASE_DIR + '/models.yaml')
example_models = example_model_generator.generate_models()