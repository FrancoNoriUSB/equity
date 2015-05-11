# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0027_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='nombre',
            field=models.CharField(max_length=100, choices=[(b'1', b'Superior'), (b'2', b'Medio-Superior'), (b'3', b'Medio-Inferior'), (b'4', b'Inferior')]),
            # preserve_default=True,
        ),
    ]
