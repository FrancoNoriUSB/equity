# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0015_auto_20141228_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, choices=[(b'Superior', b'Superior'), (b'Medio-Superior', b'Medio-Superior'), (b'Medio-Inferior', b'Medio-Inferior'), (b'Inferior', b'Inferior')])),
                ('imagen', models.ImageField(upload_to=b'slide-home/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to=b'slide-home/')),
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'verbose_name': 'Slide',
                'verbose_name_plural': 'Slides',
            },
            bases=(models.Model,),
        ),
    ]
