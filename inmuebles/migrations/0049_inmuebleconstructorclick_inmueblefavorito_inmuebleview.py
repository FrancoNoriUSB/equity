# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0048_auto_20160810_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='InmuebleConstructorClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
                ('usuario', models.ForeignKey(to='inmuebles.User')),
            ],
            options={
                'verbose_name': 'InmuebleClick',
                'verbose_name_plural': 'InmueblesClicks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleFavorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
                ('usuario', models.ForeignKey(to='inmuebles.User')),
            ],
            options={
                'verbose_name': 'InmuebleFavorito',
                'verbose_name_plural': 'InmueblesFavoritos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'InmuebleView',
                'verbose_name_plural': 'InmueblesViews',
            },
            bases=(models.Model,),
        ),
    ]
