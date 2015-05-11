# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0024_auto_20150101_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agente',
            options={'ordering': ('nombre',), 'verbose_name': 'Agente', 'verbose_name_plural': 'Agentes'},
        ),
        migrations.AlterModelOptions(
            name='modulo',
            options={'ordering': ('precio',), 'verbose_name': 'Modulo', 'verbose_name_plural': 'Modulos'},
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='tipo_obra',
            field=models.CharField(max_length=20, choices=[(b'Pre-venta', b'Pre-venta'), ('En Construcci\xf3n', 'En Construcci\xf3n'), (b'Listo Para Entregar', b'Listo Para Entregar')]),
            # preserve_default=True,
        ),
        # migrations.AlterField(
        #     model_name='moneda',
        #     name='tasa',
        #     field=models.DecimalField(max_digits=20, decimal_places=2),
        #     # preserve_default=True,
        # ),
        migrations.AlterField(
            model_name='telefonoagente',
            name='tipo',
            field=models.CharField(max_length=20, choices=[(b'Celular', b'Celular'), ('Tel\xe9fono', 'Tel\xe9fono')]),
            # preserve_default=True,
        ),
    ]
