# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0041_agente_correo2'),
    ]

    operations = [
        migrations.AddField(
            model_name='pais',
            name='orden',
            field=models.IntegerField(default=1, max_length=2, editable=False),
            preserve_default=True,
        ),
    ]
