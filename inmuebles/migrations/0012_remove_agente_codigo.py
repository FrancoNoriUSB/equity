# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0011_auto_20141224_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agente',
            name='codigo',
        ),
    ]
