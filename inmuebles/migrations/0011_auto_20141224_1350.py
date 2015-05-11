# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0010_auto_20141222_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='fecha_entrega',
            field=models.DateField(),
            # preserve_default=True,
        ),
    ]
