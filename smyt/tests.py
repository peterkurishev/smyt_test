# -*- coding: utf-8 -*-
__author__ = 'Peter A. Kurishev'

# Create your tests here.

from django.test import TestCase
from django.db import models

import unittest
from django.test import Client
import json

from smyt.models import SmytModelGenerator

#Test data definitions
ADD_USER_URL = '/smyt/a/users'
UPDATE_USER_URL = '/smyt/u/users'
GET_USERS_URL = '/smyt/m/users'
ADD_ROOM_URL = '/smyt/a/rooms'
GET_ROOMS_URL = '/smyt/m/rooms'
UPDATE_ROOM_URL = '/smyt/u/rooms'

DATE_JOINED_1 = '01/01/2014'
PAYCHECK_1 = 12345
NAME_1 = 'Test User'

DATE_JOINED_2 = '2000-01-01'
PAYCHECK_2 = 200000
NAME_2 = 'Changed Name'

DEPT_1 = 'Departament 1'
SPOTS_1 = 2

DEPT_2 = 'Departament 2'
SPOTS_2 = 3

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

    def test_models_list(self):
        response = self.client.get('/smyt/')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        post_data = {
            'name': NAME_1,
            'paycheck': PAYCHECK_1,
            'date_joined': DATE_JOINED_1,
        }
        response = self.client.post(ADD_USER_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_USERS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data['objects']), 1)

    def test_update_user_name(self):
        post_data = {
            'pk': 1,
            'field': 'name',
            'value': NAME_2,
            }
        response = self.client.post(UPDATE_USER_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_USERS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(json_data['objects'][0]['id'], 1)
        self.assertEqual(json_data['objects'][0]['name'], NAME_2)

    def test_update_user_paycheck(self):
        post_data = {
            'pk': 1,
            'field': 'paycheck',
            'value': PAYCHECK_2,
            }
        response = self.client.post(UPDATE_USER_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_USERS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(json_data['objects'][0]['id'], 1)
        self.assertEqual(json_data['objects'][0]['paycheck'], PAYCHECK_2)

    def test_update_user_date_joined(self):
        post_data = {
            'pk': 1,
            'field': 'date_joined',
            'value': '2000-01-01',
            }
        response = self.client.post(UPDATE_USER_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_USERS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(json_data['objects'][0]['id'], 1)
        self.assertEqual(json_data['objects'][0]['date_joined'], '2000-01-01')

    def test_add_room(self):
        post_data = {
            'department': DEPT_1,
            'spots': SPOTS_1,
            }
        response = self.client.post(ADD_ROOM_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_ROOMS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content)
        self.assertEqual(len(json_data['objects']), 1)

    def test_update_room_dept(self):
        post_data = {
            'pk': 1,
            'field': 'department',
            'value': DEPT_2,
            }
        response = self.client.post(UPDATE_ROOM_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_ROOMS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(json_data['objects'][0]['id'], 1)
        self.assertEqual(json_data['objects'][0]['department'], DEPT_2)

    def test_update_room_spots(self):
        post_data = {
            'pk': 1,
            'field': 'spots',
            'value': SPOTS_2,
            }
        response = self.client.post(UPDATE_ROOM_URL, data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)

        response = self.client.get(GET_ROOMS_URL, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        json_data = json.loads(response.content)
        self.assertEqual(json_data['objects'][0]['id'], 1)
        self.assertEqual(json_data['objects'][0]['spots'], SPOTS_2)
