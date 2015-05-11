# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0005_auto_20141217_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'A', max_length=30)),
                ('metros', models.CharField(max_length=10)),
                ('banos', models.CharField(max_length=2)),
                ('dormitorios', models.CharField(max_length=2)),
                ('estacionamientos', models.CharField(max_length=2)),
                ('precio', models.DecimalField(max_digits=25, decimal_places=2)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Modulos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('tasa', models.DecimalField(max_digits=20, decimal_places=2)),
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'verbose_name': 'Moneda',
                'verbose_name_plural': 'Monedas',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='inmueble',
            name='banos',
        ),
        migrations.RemoveField(
            model_name='inmueble',
            name='estacionamiento',
        ),
        migrations.RemoveField(
            model_name='inmueble',
            name='habitaciones',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='fecha_entrega',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 17, 19, 40, 26, 190000, tzinfo=utc)),
            # preserve_default=False,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='logo',
            field=models.ImageField(default='uploads/logos_inmuebles/logo.png', upload_to=b'logos_inmuebles/'),
            # preserve_default=False,
        ),
        migrations.AddField(
            model_name='inmueble',
            name='tipo_obra',
            field=models.CharField(default='Pre-venta', max_length=20, choices=[(b'Pre-venta', b'Pre-venta'), (b'En Construccion', 'En Construcci\xf3n'), (b'Listo por entregar', b'Listo Para Entregar')]),
            # preserve_default=False,
        ),
    ]
