# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0007_modulo_plano'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agente',
            name='usuario',
        ),
        migrations.AddField(
            model_name='agente',
            name='correo',
            field=models.CharField(default='', max_length=40),
            # preserve_default=False,
        ),
        migrations.AddField(
            model_name='agente',
            name='nombre',
            field=models.CharField(default='', max_length=30),
            # preserve_default=False,
        ),
        migrations.AddField(
            model_name='imageninmueble',
            name='principal',
            field=models.BooleanField(default=True, help_text=b'Marcado si desea que se muestre como imagen principal'),
            # preserve_default=True,
        ),
        migrations.AddField(
            model_name='telefonoagente',
            name='tipo',
            field=models.CharField(default='Celular', max_length=20, choices=[(b'Celular', b'Celular'), (b'Local', b'Local')]),
            # preserve_default=False,
        ),
    ]
