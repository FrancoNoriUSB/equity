# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0003_auto_20141110_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='logo',
            field=models.ImageField(upload_to=b'uploads/img/agentes'),
            # preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imageninmueble',
            name='thumbnail',
            field=models.ImageField(upload_to=b'uploads/img/thumbnails/', null=True, editable=False, blank=True),
            # preserve_default=True,
        ),
    ]
