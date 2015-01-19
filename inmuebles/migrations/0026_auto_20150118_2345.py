# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0025_auto_20150106_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='pagina',
            field=models.CharField(default=b'', max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modulo',
            name='banos',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modulo',
            name='dormitorios',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modulo',
            name='estacionamientos',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
    ]
