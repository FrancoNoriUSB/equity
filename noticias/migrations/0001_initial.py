# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inmuebles', '0001_initial'),
    ]

    operations = [
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
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
            },
            bases=(models.Model,),
        ),
    ]
