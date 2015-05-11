# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0002_auto_20141107_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(upload_to=b'uploads/img/')),
                ('thumbnail', models.ImageField(null=True, upload_to=b'uploads/img/thumbnails/', blank=True)),
                ('descripcion', models.CharField(max_length=140, null=True)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'ordering': ('imagen',),
                'abstract': False,
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TelefonoAgente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=30)),
                ('agente', models.ForeignKey(related_name='telefonos', to='inmuebles.Agente')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Telefono Agente',
                'verbose_name_plural': 'Telefonos Agentes',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='imagen',
            name='inmueble',
        ),
        migrations.DeleteModel(
            name='Imagen',
        ),
        migrations.RemoveField(
            model_name='telefono',
            name='agente',
        ),
        migrations.DeleteModel(
            name='Telefono',
        ),
        migrations.AlterModelOptions(
            name='agente',
            options={'verbose_name': 'Agente', 'verbose_name_plural': 'Agentes'},
        ),
        migrations.AlterModelOptions(
            name='campoinmueble',
            options={'verbose_name': 'Campo Inmueble', 'verbose_name_plural': 'Campos Inmueble'},
        ),
        migrations.AlterModelOptions(
            name='campotipoinmueble',
            options={'verbose_name': 'Campo Tipo Inmueble', 'verbose_name_plural': 'Campos Tipo Inmueble'},
        ),
        migrations.AlterModelOptions(
            name='inmueble',
            options={'verbose_name': 'Inmueble', 'verbose_name_plural': 'Inmuebles'},
        ),
        migrations.AlterModelOptions(
            name='tipoinmueble',
            options={'verbose_name': 'Tipo Inmueble', 'verbose_name_plural': 'Tipos Inmuebles'},
        ),
        migrations.AlterModelOptions(
            name='valorcampoinmueble',
            options={'verbose_name': 'Valor Campo Inmueble', 'verbose_name_plural': 'Valor Campos Inmueble'},
        ),
        migrations.AlterModelOptions(
            name='valorcampotipoinmueble',
            options={'verbose_name': 'Valor Campo Tipo Inmueble', 'verbose_name_plural': 'Valor Campos Tipo Inmueble'},
        ),
        migrations.AlterField(
            model_name='valorcampoinmueble',
            name='valor',
            field=models.CharField(max_length=150),
            # preserve_default=True,
        ),
    ]
