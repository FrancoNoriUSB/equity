# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0038_inmueble_areas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmueble',
            name='areas_comunes',
        ),
    ]
