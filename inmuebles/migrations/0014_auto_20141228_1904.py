# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0013_auto_20141226_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageninmueble',
            name='inmueble',
            field=models.ForeignKey(related_name='imagenes', to='inmuebles.Inmueble'),
            # preserve_default=True,
        ),
    ]
