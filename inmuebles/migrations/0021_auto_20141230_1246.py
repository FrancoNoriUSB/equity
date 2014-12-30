# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0020_auto_20141230_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='agente',
            field=models.ForeignKey(to='inmuebles.Agente', null=True),
            preserve_default=True,
        ),
    ]
