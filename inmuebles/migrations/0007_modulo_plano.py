# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0006_auto_20141217_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='plano',
            field=models.ImageField(default='uploads/planos/plano.png', upload_to=b'uploads/planos/'),
            # preserve_default=False,
        ),
    ]
