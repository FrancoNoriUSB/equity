# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('posicion', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'ordering': ('pais',),
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=80)),
                ('cuerpo', models.TextField(max_length=6000)),
                ('imagen', models.ImageField(upload_to=b'')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
            },
            bases=(models.Model,),
        ),
    ]
