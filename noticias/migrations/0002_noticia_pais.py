# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0004_auto_20141116_1831'),
        ('noticias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='pais',
            field=models.ForeignKey(default=1, to='inmuebles.Pais'),
            preserve_default=False,
        ),
    ]
