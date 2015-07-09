# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0036_auto_20150702_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulo',
            name='metraje',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='archivo',
            field=models.FileField(null=True, upload_to=b'archivos_inmuebles/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='forma_pago',
            field=models.TextField(max_length=100, null=True, verbose_name=b'Forma de pago', blank=True),
            preserve_default=True,
        ),
    ]
