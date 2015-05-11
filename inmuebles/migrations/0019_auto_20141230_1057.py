# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0018_auto_20141229_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='fecha_entrega',
            field=models.CharField(max_length=20),
            # preserve_default=True,
        ),
    ]
