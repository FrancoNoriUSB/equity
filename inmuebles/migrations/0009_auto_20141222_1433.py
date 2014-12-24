# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0008_auto_20141218_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneda',
            name='tasa',
            field=models.DecimalField(max_digits=20, decimal_places=4),
            preserve_default=True,
        ),
    ]
