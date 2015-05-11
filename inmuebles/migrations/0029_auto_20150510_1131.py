# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0028_auto_20150217_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='correo',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='agente',
            name='nombre',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='banner',
            name='url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='logo',
            field=models.ImageField(upload_to=b'logos_inmuebles/'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='simbolo',
            field=models.CharField(max_length=10),
        ),
    ]
