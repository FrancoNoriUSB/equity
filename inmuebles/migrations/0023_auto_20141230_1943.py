# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0022_auto_20141230_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneda',
            name='simbolo',
            field=models.CharField(default='$', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imageninmueble',
            name='imagen',
            field=models.ImageField(null=True, upload_to=b'uploads/img/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='tipo_obra',
            field=models.CharField(max_length=20, choices=[(b'Pre-venta', b'Pre-venta'), ('En Construcci\xf3n', 'En Construcci\xf3n'), (b'Listo Por entregar', b'Listo Por Entregar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='telefonoagente',
            name='tipo',
            field=models.CharField(max_length=20, choices=[(b'Celular', b'Celular'), (b'Tel\xc3\xa9fono', b'Telefono')]),
            preserve_default=True,
        ),
    ]
