# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0034_auto_20150701_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='metraje',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
