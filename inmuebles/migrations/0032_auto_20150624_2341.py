# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0031_inmueble_pagina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='inmueble',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='video',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
