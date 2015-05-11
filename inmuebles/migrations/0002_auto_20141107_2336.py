# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorCampoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(max_length=20)),
                ('campo', models.ForeignKey(to='inmuebles.CampoInmueble')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='campoinmueble',
            name='inmueble',
        ),
        migrations.RemoveField(
            model_name='campoinmueble',
            name='valor',
        ),
        migrations.AddField(
            model_name='campoinmueble',
            name='tipo',
            field=models.CharField(default=b'T', max_length=1, choices=[(b'N', b'N\xc3\xbamero'), (b'T', b'Texto')]),
            # preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagen',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=b''),
            # preserve_default=False,
        ),
        migrations.AlterField(
            model_name='campoinmueble',
            name='nombre',
            field=models.CharField(max_length=80),
            # preserve_default=True,
        ),
    ]
