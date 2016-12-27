# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0056_auto_20161012_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnlaceComercial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('enlace', models.CharField(max_length=200)),
                ('codigo', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Enlace Comercial',
                'verbose_name_plural': 'Enlaces Comerciales',
            },
            bases=(models.Model,),
        ),
    ]
