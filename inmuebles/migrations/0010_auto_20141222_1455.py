# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0009_auto_20141222_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='codigo',
            field=models.CharField(unique=True, max_length=20),
            preserve_default=True,
        ),
    ]
