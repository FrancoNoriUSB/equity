# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0043_auto_20160217_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inmueble',
            old_name='plano',
            new_name='archivo',
        ),
        migrations.RenameField(
            model_name='inmueble',
            old_name='ficha_tecnina',
            new_name='ficha_tecnica',
        ),
    ]
