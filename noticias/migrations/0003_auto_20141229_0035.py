# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_noticia_pais'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='pais',
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
    ]
