# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0052_inmuebleskypeclick'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inmuebleconstructorclick',
            options={'verbose_name': 'Inmueble Click', 'verbose_name_plural': 'Inmuebles Clicks'},
        ),
        migrations.AlterModelOptions(
            name='inmuebleskypeclick',
            options={'verbose_name': 'Inmueble Skype Click', 'verbose_name_plural': 'Inmuebles Skype Clicks'},
        ),
        migrations.AlterModelOptions(
            name='inmuebleview',
            options={'verbose_name': 'Inmueble View', 'verbose_name_plural': 'Inmuebles Views'},
        ),
    ]
