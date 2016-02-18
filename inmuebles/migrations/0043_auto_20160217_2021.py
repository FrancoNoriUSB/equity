# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0042_pais_orden'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ciudad',
            options={'ordering': ('nombre',), 'verbose_name': 'Ciudad', 'verbose_name_plural': 'Ciudades'},
        ),
        migrations.AlterModelOptions(
            name='zona',
            options={'ordering': ('nombre',), 'verbose_name': 'Zona', 'verbose_name_plural': 'Zonas'},
        ),
        migrations.RenameField(
            model_name='inmueble',
            old_name='feche_actualizacion',
            new_name='fecha_actualizacion',
        ),
        migrations.RenameField(
            model_name='inmueble',
            old_name='archivo',
            new_name='plano',
        ),
        migrations.AddField(
            model_name='inmueble',
            name='ficha_tecnina',
            field=models.FileField(null=True, upload_to=b'fichas_inmuebles/', blank=True),
            preserve_default=True,
        ),
    ]
