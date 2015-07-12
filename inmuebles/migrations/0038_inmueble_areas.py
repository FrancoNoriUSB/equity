# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
def create_inmueble_areas(apps, schema_editor):

    Inmueble = apps.get_model("inmuebles", "Inmueble")
    for inmueble in Inmueble.objects.all():
        areas = ''
        areas_comunes = inmueble.areas_comunes.all()
        for area in areas_comunes:
            if area == areas_comunes[len(areas_comunes)-1]:
                areas= areas + str(area.nombre) +'.'
            else:
                areas= areas + str(area.nombre) +', '

        inmueble.areas = areas
        inmueble.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0037_auto_20150708_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='areas',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.RunPython(create_inmueble_areas),
    ]
