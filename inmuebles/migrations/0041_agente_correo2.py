# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0040_auto_20150712_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='agente',
            name='correo2',
            field=models.CharField(default=b'', max_length=40, null=True),
            preserve_default=True,
        ),
    ]
