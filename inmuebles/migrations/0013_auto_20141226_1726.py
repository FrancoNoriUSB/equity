# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0012_remove_agente_codigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaComun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Area Comun',
                'verbose_name_plural': 'Area Comunes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inmueble',
            name='areas_comunes',
            field=models.ManyToManyField(to='inmuebles.AreaComun'),
            preserve_default=True,
        ),
    ]
