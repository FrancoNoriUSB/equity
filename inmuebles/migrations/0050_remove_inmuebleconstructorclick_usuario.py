# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0049_inmuebleconstructorclick_inmueblefavorito_inmuebleview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmuebleconstructorclick',
            name='usuario',
        ),
    ]
