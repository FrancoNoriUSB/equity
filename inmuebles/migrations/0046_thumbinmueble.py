# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0045_auto_20160315_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'uploads/img/')),
                ('thumbnail', models.ImageField(upload_to=b'uploads/img/thumbnails/', null=True, editable=False, blank=True)),
                ('descripcion', models.CharField(max_length=140, null=True)),
                ('principal', models.BooleanField(default=True, help_text=b'Marcado si desea que se muestre como imagen principal')),
                ('inmueble', models.ForeignKey(related_name=b'thumbnails', to='inmuebles.Inmueble')),
            ],
            options={
                'ordering': ('imagen',),
                'abstract': False,
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
            },
            bases=(models.Model,),
        ),
    ]
