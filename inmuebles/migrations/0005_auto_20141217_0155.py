# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0004_auto_20141116_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='banos',
            field=models.IntegerField(default=0, max_length=2),
            # preserve_default=True,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='estacionamiento',
            field=models.IntegerField(default=0, max_length=2),
            # preserve_default=True,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='habitaciones',
            field=models.IntegerField(default=0, max_length=2),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agente',
            name='logo',
            field=models.ImageField(upload_to=b'agentes/'),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='latitud',
            field=models.DecimalField(max_digits=20, decimal_places=17),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='longitud',
            field=models.DecimalField(max_digits=20, decimal_places=17),
            # preserve_default=True,
        ),
    ]
