# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0051_auto_20160812_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='InmuebleSkypeClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'InmuebleSkypeClick',
                'verbose_name_plural': 'InmueblesSkypeClicks',
            },
            bases=(models.Model,),
        ),
    ]
