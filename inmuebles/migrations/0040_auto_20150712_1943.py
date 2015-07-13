# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0039_remove_inmueble_areas_comunes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inmueble',
            old_name='areas',
            new_name='areas_comunes',
        ),
    ]
