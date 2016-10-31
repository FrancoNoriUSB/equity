# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0055_auto_20160817_0954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ciudad',
            options={'ordering': ('prioridad',), 'verbose_name': 'Ciudad', 'verbose_name_plural': 'Ciudades'},
        ),
        migrations.AlterModelOptions(
            name='inmueblefavorito',
            options={'verbose_name': 'Inmueble Favorito', 'verbose_name_plural': 'Inmuebles Favoritos'},
        ),
        migrations.AddField(
            model_name='ciudad',
            name='prioridad',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=True,
        ),
    ]
