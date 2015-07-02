# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0035_modulo_metraje'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulo',
            options={'ordering': ('precio', 'metros'), 'verbose_name': 'Modulo', 'verbose_name_plural': 'Modulos'},
        ),
        migrations.AlterField(
            model_name='modulo',
            name='metros',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
