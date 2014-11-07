# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=40)),
                ('logo', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('valor', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampoTipoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
                ('tipo', models.CharField(default=b'T', max_length=1, choices=[(b'N', b'N\xc3\xbamero'), (b'T', b'Texto')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=150)),
                ('latitud', models.DecimalField(max_digits=8, decimal_places=6)),
                ('longitud', models.DecimalField(max_digits=8, decimal_places=6)),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('feche_actualizacion', models.DateTimeField(auto_now=True)),
                ('fecha_expiracion', models.DateTimeField()),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
                ('ciudad', models.ForeignKey(to='inmuebles.Ciudad')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', django_countries.fields.CountryField(max_length=2)),
            ],
            options={
                'verbose_name': 'Pais',
                'verbose_name_plural': 'Paises',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telefono', models.CharField(max_length=50)),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValorCampoTipoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(max_length=150)),
                ('campo', models.ForeignKey(to='inmuebles.CampoTipoInmueble')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
                ('ciudad', models.ForeignKey(to='inmuebles.Ciudad')),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inmueble',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='tipo',
            field=models.ForeignKey(to='inmuebles.TipoInmueble'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='zona',
            field=models.ForeignKey(to='inmuebles.Zona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagen',
            name='inmueble',
            field=models.ForeignKey(to='inmuebles.Inmueble'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ciudad',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campotipoinmueble',
            name='tipo_inmueble',
            field=models.ForeignKey(to='inmuebles.TipoInmueble'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campoinmueble',
            name='inmueble',
            field=models.ForeignKey(to='inmuebles.Inmueble'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agente',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agente',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
