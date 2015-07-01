# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.template.defaultfilters import slugify

def create_inmueble_slug(apps, schema_editor):
    # We can't import the Category model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Inmueble = apps.get_model("inmuebles", "Inmueble")
    for inmueble in Inmueble.objects.all():
        inmueble.slug = slugify(inmueble.titulo)
        inmueble.save()


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0032_auto_20150624_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='slug',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='titulo',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.RunPython(create_inmueble_slug),
    ]
