# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0047_auto_20160807_1045'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cedula',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='user',
            name='telefono',
        ),
    ]
