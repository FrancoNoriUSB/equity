# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0023_auto_20141230_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='tipo_obra',
            field=models.CharField(max_length=20, choices=[(b'Pre-venta', b'Pre-venta'), ('En Construcci\xf3n', 'En Construcci\xf3n'), (b'Listo Por Entregar', b'Listo Por Entregar')]),
            # preserve_default=True,
        ),
        # migrations.AlterField(
        #     model_name='modulo',
        #     name='precio',
        #     field=models.DecimalField(max_digits=25, decimal_places=2),
        #     # preserve_default=True,
        # ),
        migrations.AlterField(
            model_name='telefonoagente',
            name='tipo',
            field=models.CharField(max_length=20, choices=[(b'Celular', b'Celular'), (b'Tel\xc3\xa9fono', b'Tel\xc3\xa9fono')]),
            # preserve_default=True,
        ),
    ]
