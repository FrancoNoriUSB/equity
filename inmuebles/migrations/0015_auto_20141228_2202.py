# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0014_auto_20141228_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneda',
            name='pais',
            field=models.OneToOneField(to='inmuebles.Pais'),
            preserve_default=True,
        ),
    ]
