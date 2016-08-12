# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0050_remove_inmuebleconstructorclick_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='forma_pago',
            field=models.TextField(max_length=300, null=True, verbose_name=b'Forma de pago', blank=True),
        ),
    ]
