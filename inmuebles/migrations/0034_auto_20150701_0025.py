# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0033_auto_20150701_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='slug',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
