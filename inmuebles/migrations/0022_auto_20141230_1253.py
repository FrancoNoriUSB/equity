# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0021_auto_20141230_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='agente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inmuebles.Agente', null=True),
            # preserve_default=True,
        ),
    ]
