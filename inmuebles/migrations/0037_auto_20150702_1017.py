# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0035_modulo_metraje'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulo',
            name='metraje',
        ),
        migrations.AlterField(
            model_name='modulo',
            name='metros',
            field=models.IntegerField(max_length=10),
        ),
    ]
