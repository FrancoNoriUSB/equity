# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0019_auto_20141230_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulo',
            name='plano',
            field=models.ImageField(null=True, upload_to=b'uploads/planos/'),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='telefonoagente',
            name='tipo',
            field=models.CharField(max_length=20, choices=[(b'Celular', b'Celular'), (b'Telefono', b'Tel\xc3\xa9fono')]),
            # preserve_default=True,
        ),
    ]
