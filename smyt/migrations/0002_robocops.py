# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smyt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='robocops',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('height', models.IntegerField(verbose_name='\u0420\u043e\u0441\u0442')),
                ('wight', models.IntegerField(verbose_name='\u0412\u0435\u0441')),
            ],
            options={
                'verbose_name': '\u0420\u043e\u0431\u043e\u043a\u043e\u043f\u044b',
                'verbose_name_plural': '\u0420\u043e\u0431\u043e\u043a\u043e\u043f\u044b',
            },
            bases=(models.Model,),
        ),
    ]
