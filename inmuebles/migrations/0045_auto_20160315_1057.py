# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0044_auto_20160217_2024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='areacomun',
            options={'verbose_name': 'Area Comun', 'verbose_name_plural': 'Areas Comunes'},
        ),
        migrations.AddField(
            model_name='inmueble',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
