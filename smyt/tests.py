# -*- coding: utf-8 -*-
__author__ = 'Peter A. Kurishev'

# Create your tests here.

from django.test import TestCase
from django.db import models

import unittest
from django.test import Client
import json

from smyt.models import SmytModelGenerator


class SmytModelTestCase(TestCase):
    def prepare_model(self):
        yaml_string = """
users:
  title: Пользователи
  fields:
    - {id: name, title: Имя, type: char}
    - {id: paycheck, title: Зарплата, type: int}
    - {id: date_joined, title: Дата поступления на работу, type: date}

"""

        test_model_generator = SmytModelGenerator()
        test_model_generator.init_from_string(yaml_string)
        return test_model_generator.generate_models()[0]

    def test_model_is_created(self):
        test_model = self.prepare_model()
        self.assertIsNotNone(test_model)

    def test_model_name_is_correct(self):
        test_model = self.prepare_model()
        self.assertEqual(test_model.__name__, 'users')

    def test_model_title_is_correct(self):
        test_model = self.prepare_model()
        self.assertEqual(test_model._meta.verbose_name.title(), 'Пользователи'.decode('utf-8'))

    def test_fields_are_created(self):
        test_model = self.prepare_model()
        self.assertIn('name', [f.name for f in test_model._meta.fields])
        self.assertIn('paycheck', [f.name for f in test_model._meta.fields])
        self.assertIn('date_joined', [f.name for f in test_model._meta.fields])

    def test_field_types_are_correct(self):
        test_model = self.prepare_model()
        self.assertIsInstance(test_model._meta.get_field('name'), models.CharField)
        self.assertIsInstance(test_model._meta.get_field('paycheck'), models.IntegerField)
        self.assertIsInstance(test_model._meta.get_field('date_joined'), models.DateField)

    def test_field_titles_are_correct(self):
        test_model = self.prepare_model()
        self.assertEqual(test_model._meta.get_field('name').verbose_name.title(), 'Имя'.decode('utf-8'))
        self.assertEqual(test_model._meta.get_field('paycheck').verbose_name.title(), 'Зарплата'.decode('utf-8'))
        self.assertTrue(test_model._meta.get_field('date_joined').verbose_name.title(),
                        'Дата поступления на работу'.decode('utf-8'))


class SmytRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        # self.client.get('/smyt/f/users')
        # print self.client.cookies
        #
        # self.csrf_token = self.client.cookies['csrftoken'].value

    def test_models_list(self):
        response = self.client.get('/smyt/')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        post_data = {
            'name': 'Test User',
            'paycheck': 12345,
            'date_joined': '01/01/2014',
        }
        response = self.client.post('/smyt/a/users', data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/smyt/m/users', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(len(json_data['objects']), 1)
