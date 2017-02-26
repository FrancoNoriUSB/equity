# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
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
                ('nombre', models.CharField(max_length=30)),
                ('correo', models.CharField(max_length=40)),
                ('correo2', models.CharField(default=b'', max_length=40, null=True)),
                ('pagina', models.CharField(default=b'', max_length=100, null=True)),
                ('logo', models.ImageField(upload_to=b'agentes/')),
            ],
            options={
                'ordering': ('nombre',),
                'verbose_name': 'Agente',
                'verbose_name_plural': 'Agentes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaComun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Area Comun',
                'verbose_name_plural': 'Areas Comunes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, choices=[(b'1', b'Superior'), (b'2', b'Medio-Superior'), (b'3', b'Medio-Inferior'), (b'4', b'Inferior')])),
                ('imagen', models.ImageField(upload_to=b'slide-home/')),
                ('url', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
                ('tipo', models.CharField(default=b'T', max_length=1, choices=[(b'N', b'N\xc3\xbamero'), (b'T', b'Texto')])),
            ],
            options={
                'verbose_name': 'Campo Inmueble',
                'verbose_name_plural': 'Campos Inmueble',
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
                'verbose_name': 'Campo Tipo Inmueble',
                'verbose_name_plural': 'Campos Tipo Inmueble',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
                ('prioridad', models.IntegerField(default=0, max_length=2)),
            ],
            options={
                'ordering': ('prioridad',),
                'verbose_name': 'Ciudad',
                'verbose_name_plural': 'Ciudades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=30)),
                ('ciudad', models.ForeignKey(to='inmuebles.Ciudad')),
            ],
            options={
                'verbose_name': 'Contacto',
                'verbose_name_plural': 'Contactos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnlaceComercial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100)),
                ('enlace', models.CharField(max_length=200)),
                ('codigo', models.CharField(unique=True, max_length=10)),
            ],
            options={
                'verbose_name': 'Enlace Comercial',
                'verbose_name_plural': 'Enlaces Comerciales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagenInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'uploads/img/')),
                ('thumbnail', models.ImageField(upload_to=b'uploads/img/thumbnails/', null=True, editable=False, blank=True)),
                ('descripcion', models.CharField(max_length=140, null=True)),
                ('principal', models.BooleanField(default=True, help_text=b'Marcado si desea que se muestre como imagen principal')),
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
            name='Inmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(unique=True, max_length=100)),
                ('slug', models.CharField(unique=True, max_length=200)),
                ('codigo', models.CharField(unique=True, max_length=20)),
                ('descripcion', models.TextField()),
                ('fecha_entrega', models.CharField(max_length=20)),
                ('tipo_obra', models.CharField(max_length=20, choices=[(b'Pre-venta', b'Pre-venta'), ('En Construcci\xf3n', 'En Construcci\xf3n'), (b'Listo Para Entregar', b'Listo Para Entregar')])),
                ('direccion', models.CharField(max_length=150)),
                ('latitud', models.DecimalField(max_digits=20, decimal_places=17)),
                ('longitud', models.DecimalField(max_digits=20, decimal_places=17)),
                ('logo', models.ImageField(upload_to=b'logos_inmuebles/')),
                ('visible', models.BooleanField(default=True)),
                ('archivo', models.FileField(null=True, upload_to=b'archivos_inmuebles/', blank=True)),
                ('ficha_tecnica', models.FileField(null=True, upload_to=b'fichas_inmuebles/', blank=True)),
                ('forma_pago', models.TextField(max_length=300, null=True, verbose_name=b'Forma de pago', blank=True)),
                ('pagina', models.CharField(max_length=200, null=True, blank=True)),
                ('video', models.CharField(max_length=200, null=True, blank=True)),
                ('areas_comunes', models.TextField()),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('fecha_expiracion', models.DateTimeField()),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inmuebles.Agente', null=True)),
                ('ciudad', models.ForeignKey(to='inmuebles.Ciudad')),
            ],
            options={
                'verbose_name': 'Inmueble',
                'verbose_name_plural': 'Inmuebles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleConstructorClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'Inmueble Click',
                'verbose_name_plural': 'Inmuebles Clicks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleFavorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inmueble Favorito',
                'verbose_name_plural': 'Inmuebles Favoritos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleSkypeClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('agente', models.ForeignKey(to='inmuebles.Agente')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'Inmueble Skype Click',
                'verbose_name_plural': 'Inmuebles Skype Clicks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InmuebleView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(default=0, max_length=20)),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'Inmueble View',
                'verbose_name_plural': 'Inmuebles Views',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(default=b'A', max_length=30)),
                ('metros', models.DecimalField(max_digits=10, decimal_places=2)),
                ('banos', models.CharField(max_length=4)),
                ('dormitorios', models.CharField(max_length=4)),
                ('estacionamientos', models.CharField(max_length=4)),
                ('precio', models.DecimalField(max_digits=25, decimal_places=2)),
                ('plano', models.ImageField(null=True, upload_to=b'uploads/planos/')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'ordering': ('precio', 'metros'),
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Modulos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModuloFavorito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modulo', models.ForeignKey(to='inmuebles.Modulo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Modulo Favorito',
                'verbose_name_plural': 'Modulos Favoritos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('simbolo', models.CharField(max_length=10)),
                ('tasa', models.DecimalField(max_digits=20, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Moneda',
                'verbose_name_plural': 'Monedas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', django_countries.fields.CountryField(max_length=2)),
                ('orden', models.IntegerField(default=1, max_length=2, editable=False)),
            ],
            options={
                'verbose_name': 'Pais',
                'verbose_name_plural': 'Paises',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('imagen', models.ImageField(upload_to=b'slide-home/')),
                ('pais', models.ForeignKey(to='inmuebles.Pais')),
            ],
            options={
                'verbose_name': 'Slide',
                'verbose_name_plural': 'Slides',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TelefonoAgente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=30)),
                ('tipo', models.CharField(max_length=20, choices=[(b'Celular', b'Celular'), ('Tel\xe9fono', 'Tel\xe9fono')])),
                ('agente', models.ForeignKey(related_name='telefonos', to='inmuebles.Agente')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Telefono Agente',
                'verbose_name_plural': 'Telefonos Agentes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThumbInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagen', models.ImageField(null=True, upload_to=b'uploads/img/')),
                ('thumbnail', models.ImageField(upload_to=b'uploads/img/thumbnails/', null=True, editable=False, blank=True)),
                ('descripcion', models.CharField(max_length=140, null=True)),
                ('principal', models.BooleanField(default=True, help_text=b'Marcado si desea que se muestre como imagen principal')),
                ('inmueble', models.ForeignKey(related_name='thumbnails', to='inmuebles.Inmueble')),
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
            name='TipoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': 'Tipo Inmueble',
                'verbose_name_plural': 'Tipos Inmuebles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValorCampoInmueble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor', models.CharField(max_length=150)),
                ('campo', models.ForeignKey(to='inmuebles.CampoInmueble')),
                ('inmueble', models.ForeignKey(to='inmuebles.Inmueble')),
            ],
            options={
                'verbose_name': 'Valor Campo Inmueble',
                'verbose_name_plural': 'Valor Campos Inmueble',
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
                'verbose_name': 'Valor Campo Tipo Inmueble',
                'verbose_name_plural': 'Valor Campos Tipo Inmueble',
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
                'ordering': ('nombre',),
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='moneda',
            name='pais',
            field=models.OneToOneField(to='inmuebles.Pais'),
            preserve_default=True,
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
            model_name='imageninmueble',
            name='inmueble',
            field=models.ForeignKey(related_name='imagenes', to='inmuebles.Inmueble'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contacto',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
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
            model_name='banner',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agente',
            name='pais',
            field=models.ForeignKey(to='inmuebles.Pais'),
            preserve_default=True,
        ),
    ]
