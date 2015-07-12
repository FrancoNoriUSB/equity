# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_modulo_metraje(apps, schema_editor):
    
    Modulo = apps.get_model("inmuebles", "Modulo")
    for modulo in Modulo.objects.all():
        metros = float(str(modulo.metros).replace(',','.'))
        modulo.metraje = metros
        modulo.save()

class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0034_auto_20150701_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='metraje',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.RunPython(create_modulo_metraje),
    ]