# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0016_banner_slide'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.CharField(default='/', max_length=200),
            # preserve_default=False,
        ),
    ]
