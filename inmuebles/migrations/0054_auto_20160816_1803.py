# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0053_auto_20160815_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuloFavorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modulo', models.ForeignKey(to='inmuebles.Modulo')),
                ('usuario', models.ForeignKey(to='inmuebles.User')),
            ],
            options={
                'verbose_name': 'Modulo Favorito',
                'verbose_name_plural': 'Modulos Favoritos',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='user',
            name='apellido',
        ),
    ]
